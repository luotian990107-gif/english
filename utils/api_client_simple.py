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
        
        data = {
            "model": model or OPENAI_MODEL,
            "messages": messages,
            "max_tokens": max_tokens or MAX_TOKENS,
            "temperature": temperature or TEMPERATURE,
            "stream": stream
        }
        
        try:
            if stream:
                # 流式响应
                response = requests.post(url, headers=self.headers, json=data, stream=True, timeout=60)
                response.raise_for_status()
                
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
            else:
                # 非流式响应
                response = requests.post(url, headers=self.headers, json=data, timeout=60)
                response.raise_for_status()
                return response.json()
                
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
            if response and response.get('choices') and len(response['choices']) > 0:
                # 返回生成的文本
                return response['choices'][0]['message']['content']
            else:
                st.error("❌ API返回了空响应，请稍后再试")
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
        for chunk in client.chat_completion(
            messages=messages,
            model=model,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            stream=True
        ):
            yield chunk
                
    except Exception as e:
        error_msg = str(e)
        yield f"\n\n❌ 错误: {error_msg}"