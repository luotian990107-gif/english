"""
我是小作家模块
"""
import streamlit as st
from utils.api_client_simple import get_claude_response
from config.settings import DEFAULT_WRITING_SAMPLE


def little_writer_module():
    """
    我是小作家功能模块
    用户输入英文文本，AI进行批改并提供结构化反馈
    """
    st.header("🖋️ 我是小作家")
    
    # 引导语
    st.markdown("""
    ### 写下你的英文作品，让克劳德老师帮你批改！
    
    不要害怕犯错，每一次尝试都是进步！你可以写：
    - 📝 一段日记
    - 🌟 一个小故事
    - 💭 你的想法
    - 📧 一封信
    
    记住：**写作最重要的是表达你的想法，语法错误没关系，我们一起进步！**
    """)
    
    # 文本输入区
    user_text = st.text_area(
        "✍️ 在这里写下你的英文作品",
        value="",
        placeholder=DEFAULT_WRITING_SAMPLE,
        height=200,
        help="写下任何你想表达的内容，可以是几句话，也可以是一段文章"
    )
    
    # 添加写作提示
    with st.expander("💡 需要灵感吗？试试这些话题"):
        st.markdown("""
        - **My Day**: What did you do today?
        - **My Friend**: Tell me about your best friend
        - **My Dream**: What do you want to be when you grow up?
        - **My Hobby**: What do you like to do in your free time?
        - **My Pet**: Do you have a pet? Tell me about it!
        - **My School**: What is your school like?
        """)
    
    # 提交按钮
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        submit_button = st.button("📤 请老师批改！", type="primary", use_container_width=True)
    
    # 处理提交
    if submit_button:
        if not user_text.strip():
            st.warning("😊 请先写一些内容再提交哦！")
            return
        
        # 构建系统提示词
        system_prompt = """你是一位经验丰富、极具耐心和亲和力的小学英语老师，专门辅导中国10岁的孩子学习英语。

你的任务是批改学生写的英文段落，并提供建设性的反馈。

批改原则：
1. 永远保持积极、鼓励的态度
2. 先表扬孩子的努力和亮点
3. 用温和的方式指出错误
4. 提供清晰的改正建议
5. 适当拓展，但不要太难

你的输出必须严格遵循以下Markdown格式：

### 🌟 总体评价

[用1-2句非常鼓励的话，表扬孩子的闪光点。比如：想象力很棒！用词很有创意！敢于表达真实想法！句子结构有进步！等等。一定要具体，不要泛泛而谈]

### ✏️ 修改建议

[用表格展示需要修改的地方。如果没有错误，就选1-2个地方提供"更地道的表达"。记住：不要列出太多错误，最多3-4个即可]

| 原文 | 修改后 | 小贴士 |
|------|--------|---------|
| 原句或词组 | 修改后的版本 | 用简单的中文解释为什么这样改更好 |

### ✨ 今天学一个新知识

[选择一个与作文相关的知识点进行简单讲解。可以是：
- 一个更地道的表达方式
- 一个简单的语法规则
- 一个相关的词汇拓展
用1-2句话说明，并给出一个简单例句]

### 🎯 继续加油

[用1句话鼓励孩子继续写作，可以提供一个小建议或下次写作的方向]

记住：你的目标是让孩子爱上英语写作，而不是打击他们的信心！"""
        
        # 构建用户提示词
        prompt = f"请批改这篇英文作文：\n\n{user_text}"
        
        # 调用API获取批改结果
        response = get_claude_response(prompt, system_prompt)
        
        if response:
            # 显示批改结果
            st.markdown("---")
            st.markdown(response)
            
            # 添加互动元素
            st.markdown("---")
            st.success("🎉 你真棒！继续努力，你的英语会越来越好！")
            
            # 添加额外功能按钮
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📝 再写一篇", use_container_width=True):
                    st.info("清空上面的文本框，写下新的内容吧！")
            
            with col2:
                if st.button("💪 我要改进", use_container_width=True):
                    st.info("根据老师的建议，试着重写一遍吧！")
            
            with col3:
                if st.button("⭐ 收藏批改", use_container_width=True):
                    st.info("批改结果已显示，你可以截图保存！")
    
    # 添加写作小贴士
    with st.sidebar:
        st.markdown("### 📚 写作小贴士")
        st.markdown("""
        **开头句型：**
        - Today I want to tell you about...
        - Let me share...
        - I'd like to talk about...
        
        **连接词：**
        - First, ... Then, ... Finally, ...
        - Also, ... / Besides, ...
        - However, ... / But, ...
        
        **结尾句型：**
        - That's all about...
        - I hope you like...
        - Thank you for reading!
        """)