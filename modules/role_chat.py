"""
角色扮演聊天室模块
"""
import streamlit as st
from utils.api_client_simple import get_streaming_response
from config.settings import CHAT_ROLES


def role_chat_module():
    """
    角色扮演聊天室功能模块
    用户选择一个角色，与AI扮演的角色进行英文对话
    """
    st.header("🗣️ 角色扮演聊天室")
    
    # 引导语
    st.markdown("""
    ### 选择一个角色，开始英语对话吧！
    
    在这里，你可以和各种有趣的角色用英语聊天。不要害羞，大胆说出你的想法！
    """)
    
    # 角色选择
    selected_role = st.selectbox(
        "🎭 选择你想对话的角色",
        CHAT_ROLES,
        help="选择一个你感兴趣的角色，开始对话吧！"
    )
    
    # 初始化或重置对话历史
    if 'current_role' not in st.session_state:
        st.session_state.current_role = selected_role
        st.session_state.messages = []
    
    # 如果角色改变，重置对话
    if st.session_state.current_role != selected_role:
        st.session_state.current_role = selected_role
        st.session_state.messages = []
        # 添加欢迎消息
        welcome_msg = f"你好！我是{selected_role.split()[1]}，让我们用英语聊聊天吧！What would you like to talk about today?"
        st.session_state.messages.append({
            "role": "assistant",
            "content": welcome_msg
        })
    
    # 如果是新对话，添加欢迎消息
    if len(st.session_state.messages) == 0:
        welcome_msg = f"你好！我是{selected_role.split()[1]}，让我们用英语聊聊天吧！What would you like to talk about today?"
        st.session_state.messages.append({
            "role": "assistant",
            "content": welcome_msg
        })
    
    # 显示对话历史
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # 用户输入
    if prompt := st.chat_input("Type your message in English... (用英语输入你的消息)"):
        # 添加用户消息到历史
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })
        
        # 显示用户消息
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # 构建系统提示词
        role_name = selected_role.split()[1]  # 提取角色名称
        system_prompt = f"""你现在正在扮演角色：{selected_role}。

你的规则是：
1. 必须完全沉浸在你的角色里，无论用户说什么，你都要以{role_name}的身份和口吻回应
2. 你的对话对象是一个正在学习英语的10岁中国孩子，所以你的语言必须：
   - 使用简单的词汇和短句
   - 友好、充满鼓励
   - 偶尔使用一些有趣的表情符号
3. 绝对不要跳出角色。如果遇到不会回答的问题，就用角色的方式巧妙回避
4. 你的每条回复都应该简短，最好不要超过3句话，以便孩子能跟上
5. 可以适当地问一些简单的问题，鼓励孩子继续对话
6. 当孩子用中文时，要温柔地鼓励他们用英语，比如说 "Try to say it in English! I believe you can do it!"

记住：你现在是{role_name}，保持角色的特点和说话方式！"""
        
        # 显示AI回复
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # 获取流式响应
            for response_chunk in get_streaming_response(prompt, system_prompt):
                full_response += response_chunk
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
        
        # 添加AI回复到历史
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response
        })
    
    # 添加控制按钮
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 开始新对话", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    with col2:
        if st.button("💡 对话提示", use_container_width=True):
            st.info("""
            **对话小贴士：**
            - Hello! How are you?
            - What do you like to do?
            - Can you tell me a story?
            - What's your favorite food?
            - Where are you from?
            """)
    
    with col3:
        if st.button("📝 查看对话历史", use_container_width=True):
            if len(st.session_state.messages) > 1:
                st.info(f"你已经和{selected_role}进行了{len(st.session_state.messages)//2}轮对话！继续加油！")
            else:
                st.info("开始聊天吧！")