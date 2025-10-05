"""
简化的API客户端 - 使用requests库避免OpenAI SDK的兼容性问题
"""
import streamlit as st
import requests
import json
from config.settings import OPENAI_MODEL, MAX_TOKENS, TEMPERATURE


class SimpleAPIClient:
    """简单的API客户端"""
    
    def __init__(self, api_key: str, api_base: str = None):
        self.api_key = api_key
        self.api_base = api_base or "https://api.openai.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def chat_completion(self, messages, model=None, max_tokens=None, temperature=None, stream=False):
        """调用chat completions API"""
        url = f"{self.api_base}/chat/completions"
        
        # 构建请求数据
        data = {
            "model": model or OPENAI_MODEL,
            "messages": messages,
            "max_tokens": max_tokens or MAX_TOKENS,
            "temperature": temperature or TEMPERATURE,
            "stream": stream
        }
        
        try:
            if stream:
                # 流式响应处理
                data["stream"] = True
                response = requests.post(url, headers=self.headers, json=data, stream=True, timeout=60)
                response.raise_for_status()
                
                # 返回生成器
                def stream_generator():
                    for line in response.iter_lines():
                        if line:
                            line = line.decode('utf-8')
                            if line.startswith('data: '):
                                line = line[6:]  # 移除 "data: " 前缀
                                if line == '[DONE]':
                                    break
                                try:
                                    chunk = json.loads(line)
                                    if chunk.get('choices') and len(chunk['choices']) > 0:
                                        delta = chunk['choices'][0].get('delta', {})
                                        if delta.get('content'):
                                            yield delta['content']
                                except json.JSONDecodeError:
                                    continue
                
                # 返回生成器函数的调用结果
                return stream_generator()
                
            else:
                # 非流式响应 - 确保返回字典
                data["stream"] = False
                response = requests.post(url, headers=self.headers, json=data, timeout=60)
                response.raise_for_status()
                
                # 获取响应文本
                response_text = response.text
                
                # 尝试解析JSON
                try:
                    result = json.loads(response_text)
                except json.JSONDecodeError:
                    # 如果不是JSON，可能是流式响应格式
                    # 尝试提取内容
                    lines = response_text.strip().split('\n')
                    content_parts = []
                    
                    for line in lines:
                        if line.startswith('data: '):
                            try:
                                chunk_data = json.loads(line[6:])
                                if chunk_data.get('choices') and len(chunk_data['choices']) > 0:
                                    # 对于流式格式，尝试提取delta或message内容
                                    choice = chunk_data['choices'][0]
                                    if 'delta' in choice and 'content' in choice['delta']:
                                        content_parts.append(choice['delta']['content'])
                                    elif 'message' in choice and 'content' in choice['message']:
                                        content_parts.append(choice['message']['content'])
                            except:
                                continue
                    
                    # 如果成功提取了内容，构造标准响应格式
                    if content_parts:
                        result = {
                            'choices': [{
                                'message': {
                                    'content': ''.join(content_parts),
                                    'role': 'assistant'
                                },
                                'finish_reason': 'stop'
                            }]
                        }
                    else:
                        raise Exception(f"无法解析API响应: {response_text[:500]}")
                
                # 确保返回的是字典格式
                if not isinstance(result, dict):
                    raise Exception(f"API返回了非预期的格式: {type(result)}")
                    
                return result
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"API请求失败: {str(e)}")


def init_client(api_key: str, api_base: str = None, model: str = None):
    """
    初始化简单API客户端
    
    Args:
        api_key: API密钥
        api_base: API端点URL（可选）
        model: 模型名称（可选）
    
    Returns:
        SimpleAPIClient实例
    """
    try:
        client = SimpleAPIClient(api_key, api_base)
        
        # 保存模型名称到session state
        if model:
            st.session_state.model = model
        else:
            st.session_state.model = OPENAI_MODEL
            
        return client
    except Exception as e:
        st.error(f"初始化API客户端失败: {str(e)}")
        return None


def get_claude_response(prompt: str, system_prompt: str) -> str:
    """
    调用API获取响应
    
    Args:
        prompt: 用户输入的提示词
        system_prompt: 系统级提示词，定义AI的角色和行为
    
    Returns:
        AI生成的响应文本
    """
    # 检查客户端是否已初始化
    if 'client' not in st.session_state or st.session_state.client is None:
        st.error("❌ 请先在侧边栏输入您的API配置信息")
        return None
    
    # 获取模型名称
    model = st.session_state.get('model', OPENAI_MODEL)
    
    try:
        # 显示加载动画
        with st.spinner("克劳德正在思考中...✨"):
            # 构建消息列表
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            # 调用API
            client = st.session_state.client
            response = client.chat_completion(
                messages=messages,
                model=model,
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                stream=False
            )
            
            # 检查响应是否有效
            if response:
                # 确保是字典响应
                if not isinstance(response, dict):
                    st.error(f"❌ API返回了非预期的格式: {type(response)}")
                    return None
                    
                # 检查是否有选择项
                if response.get('choices') and len(response['choices']) > 0:
                    # 获取消息内容
                    choice = response['choices'][0]
                    if 'message' in choice and 'content' in choice['message']:
                        return choice['message']['content']
                    else:
                        st.error(f"❌ 响应格式不正确: {choice}")
                        return None
                else:
                    # 检查是否有错误信息
                    if 'error' in response:
                        st.error(f"❌ API错误: {response['error']}")
                    else:
                        st.error(f"❌ API返回了空响应: {response}")
                    return None
            else:
                st.error("❌ 未收到API响应")
                return None
            
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "api" in error_msg.lower() and "key" in error_msg.lower():
            st.error("❌ API密钥无效，请检查您的密钥是否正确")
        elif "429" in error_msg or "rate" in error_msg.lower():
            st.error("⏳ 请求太频繁，请稍后再试")
        elif "404" in error_msg or "model" in error_msg.lower():
            st.error(f"❌ 模型 {model} 不可用，请检查模型名称")
        else:
            st.error(f"❌ 调用API时出错: {error_msg}")
        return None


def get_streaming_response(prompt: str, system_prompt: str):
    """
    获取流式响应（用于聊天功能）
    
    Args:
        prompt: 用户输入的提示词
        system_prompt: 系统级提示词
    
    Yields:
        响应文本片段
    """
    # 检查客户端是否已初始化
    if 'client' not in st.session_state or st.session_state.client is None:
        yield "❌ 请先在侧边栏输入您的API配置信息"
        return
    
    # 获取模型名称
    model = st.session_state.get('model', OPENAI_MODEL)
    
    try:
        # 构建消息列表
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        # 如果有历史消息，添加到消息列表中
        if 'messages' in st.session_state and len(st.session_state.messages) > 0:
            # 只添加最近的几轮对话，避免超出token限制
            history_messages = []
            for msg in st.session_state.messages[-6:]:  # 最多保留最近3轮对话
                if msg["role"] != "system":
                    history_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            # 重构消息列表：system + history + current
            messages = [
                {"role": "system", "content": system_prompt}
            ] + history_messages + [
                {"role": "user", "content": prompt}
            ]
        
        # 调用API获取流式响应
        client = st.session_state.client
        response = client.chat_completion(
            messages=messages,
            model=model,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            stream=True
        )
        
        # 检查返回值是否为生成器
        if hasattr(response, '__iter__') and not isinstance(response, (str, dict)):
            # 是生成器，直接迭代
            for chunk in response:
                yield chunk
        else:
            # 不是生成器，可能是错误或其他格式
            yield f"❌ 意外的响应格式: {type(response)}"
                
    except Exception as e:
        error_msg = str(e)
        yield f"\n\n❌ 错误: {error_msg}"