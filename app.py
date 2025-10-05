"""
克劳德的奇妙英语屋 - 主应用程序
Claude's English Fun House - Main Application
"""
import streamlit as st
from utils.api_client_simple import init_client
from modules import story_magic_module, role_chat_module, little_writer_module
from config.settings import (
    APP_TITLE, APP_SUBTITLE, APP_DESCRIPTION, 
    MODULES, OPENAI_API_KEY, OPENAI_API_BASE, OPENAI_MODEL
)
import os


def initialize_app():
    """初始化应用程序配置"""
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 自定义CSS样式
    st.markdown("""
    <style>
    /* 主标题样式 */
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    /* 按钮样式 */
    .stButton > button {
        border-radius: 20px;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 10px rgba(0,0,0,0.2);
    }
    
    /* 文本输入框样式 */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 10px;
    }
    
    /* 选择框样式 */
    .stSelectbox > div > div > div {
        border-radius: 10px;
    }
    
    /* 侧边栏样式 */
    .css-1d391kg {
        padding-top: 1rem;
    }
    
    /* 成功消息样式 */
    .stSuccess {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)


def setup_sidebar():
    """设置侧边栏"""
    with st.sidebar:
        # Logo和标题
        st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <h1>🏠</h1>
            <h3>克劳德的奇妙英语屋</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # API配置部分
        st.markdown("### ⚙️ API配置")
        
        # API密钥输入 - 优先使用环境变量，否则使用session state
        default_api_key = OPENAI_API_KEY or st.session_state.get('api_key', '')
        api_key = st.text_input(
            "API密钥",
            type="password",
            value=default_api_key,
            placeholder="输入你的API密钥",
            help="请输入你的API密钥以使用AI功能"
        )
        
        # 高级配置（可选）
        with st.expander("🔧 高级配置（可选）"):
            default_api_base = OPENAI_API_BASE or st.session_state.get('api_base', '')
            api_base = st.text_input(
                "API端点",
                value=default_api_base,
                placeholder="https://api.openai.com/v1",
                help="自定义API端点URL（如果使用默认OpenAI API，请留空）"
            )
            
            default_model = OPENAI_MODEL or st.session_state.get('model', '')
            model_name = st.text_input(
                "模型名称",
                value=default_model,
                placeholder="gpt-3.5-turbo",
                help="指定要使用的模型名称"
            )
        
        # 连接按钮
        if st.button("🔗 连接API", type="primary", use_container_width=True):
            if api_key:
                # 保存到session state
                st.session_state.api_key = api_key
                if api_base:
                    st.session_state.api_base = api_base
                if model_name:
                    st.session_state.model = model_name
                
                # 初始化客户端
                client = init_client(
                    api_key=api_key,
                    api_base=api_base if api_base else None,
                    model=model_name if model_name else None
                )
                
                if client:
                    st.session_state.client = client
                    st.success("✅ API连接成功！")
                else:
                    st.error("❌ API连接失败，请检查配置")
            else:
                st.warning("⚠️ 请输入API密钥")
        
        # 显示连接状态
        if 'client' in st.session_state and st.session_state.client:
            st.success("🟢 已连接")
            if 'model' in st.session_state:
                st.info(f"使用模型: {st.session_state.model}")
        else:
            st.warning("🔴 未连接")
        
        st.markdown("---")
        
        # 功能选择
        st.markdown("### 🎯 选择功能")
        selected_module = st.radio(
            "选择你想使用的功能",
            options=list(MODULES.keys()),
            format_func=lambda x: MODULES[x],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # 使用说明
        st.markdown("### 📖 使用说明")
        st.markdown("""
        1. 输入你的API密钥
        2. 点击"连接API"按钮
        3. 选择想要使用的功能
        4. 开始快乐学英语！
        
        💡 **提示**: 每个功能都有详细的引导，跟着提示操作即可。
        """)
        
        st.markdown("---")
        
        # 关于部分
        with st.expander("ℹ️ 关于本应用"):
            st.markdown("""
            **克劳德的奇妙英语屋**是一个专为中国小学生设计的英语学习应用。
            
            通过AI技术，我们提供：
            - 个性化的故事创作
            - 互动式的角色对话
            - 温柔的作文批改
            
            让学习英语变得有趣而高效！
            
            ---
            Made with ❤️ for young English learners
            """)
        
        return selected_module


def main():
    """主函数"""
    # 初始化应用
    initialize_app()
    
    # 设置侧边栏并获取选择的模块
    selected_module = setup_sidebar()
    
    # 主页面标题
    st.markdown("""
    <div class='main-header'>
        <h1>🏠 克劳德的奇妙英语屋</h1>
        <p>Claude's English Fun House - 让英语学习充满乐趣！</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 检查API连接状态
    if 'client' not in st.session_state or st.session_state.client is None:
        # 显示欢迎页面
        st.markdown(APP_DESCRIPTION)
        
        st.info("""
        👋 **欢迎来到克劳德的奇妙英语屋！**
        
        请在左侧侧边栏中：
        1. 输入你的API密钥
        2. 点击"连接API"按钮
        3. 选择你想使用的功能
        
        然后就可以开始愉快的英语学习之旅啦！
        """)
        
        # 显示功能介绍卡片
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style='padding: 1.5rem; background: #f0f8ff; border-radius: 10px; text-align: center;'>
                <h3>📖 AI故事魔法屋</h3>
                <p>输入关键词，AI为你创作精彩的英文故事！</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='padding: 1.5rem; background: #fff0f5; border-radius: 10px; text-align: center;'>
                <h3>🗣️ 角色扮演聊天室</h3>
                <p>和有趣的角色用英语对话，提高口语表达！</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style='padding: 1.5rem; background: #f0fff0; border-radius: 10px; text-align: center;'>
                <h3>🖋️ 我是小作家</h3>
                <p>写英文作品，AI老师给你贴心批改和建议！</p>
            </div>
            """, unsafe_allow_html=True)
        
    else:
        # 根据选择的模块加载相应功能
        if selected_module == "story":
            story_magic_module()
        elif selected_module == "chat":
            role_chat_module()
        elif selected_module == "writer":
            little_writer_module()
        else:
            st.error("未知的功能模块")


if __name__ == "__main__":
    main()