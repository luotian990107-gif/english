"""
AI故事魔法屋模块
"""
import streamlit as st
from utils.api_client_simple import get_claude_response
from config.settings import DEFAULT_KEYWORDS


def story_magic_module():
    """
    AI故事魔法屋功能模块
    用户输入关键词，AI生成包含这些关键词的英文故事
    """
    st.header("📖 AI故事魔法屋")
    
    # 引导语
    st.markdown("""
    ### 欢迎来到故事魔法屋！
    
    在下面输入1-3个英文单词（用逗号分隔），克劳德会为你创作一个精彩的英文小故事！
    
    比如：`dragon, castle, magic` 或者 `space, robot, friend`
    """)
    
    # 关键词输入
    col1, col2 = st.columns([3, 1])
    with col1:
        keywords = st.text_input(
            "✨ 输入你的魔法关键词",
            value=DEFAULT_KEYWORDS,
            placeholder="输入1-3个英文单词，用逗号分隔",
            help="试试输入你喜欢的事物，比如动物、地点、魔法道具等"
        )
    
    with col2:
        st.write("")  # 空行对齐
        st.write("")  # 空行对齐
        generate_button = st.button("🎨 开始创作！", type="primary", use_container_width=True)
    
    # 生成故事
    if generate_button:
        if not keywords.strip():
            st.warning("😊 请先输入一些关键词哦！")
            return
        
        # 构建系统提示词
        system_prompt = """你是一位世界顶级的儿童故事作家，专门为正在学习英语的中国10岁孩子写故事。

你的任务是：
1. 根据用户提供的关键词，创作一个150-200词的英文小故事
2. 故事必须情节简单、有趣、充满想象力
3. 语言地道，但要使用适合小学生水平的词汇和语法
4. 每个关键词都必须在故事中自然地出现
5. 在故事结束后，必须用Markdown表格格式列出故事中的5个重点单词，提供中文翻译和简单的英文例句

输出格式要求：
- 首先输出一个吸引人的故事标题（用### 标记）
- 然后是故事正文（分段书写，使段落清晰）
- 最后是词汇表（使用Markdown表格）

词汇表格式：
| 单词 | 中文意思 | 例句 |
|------|---------|------|
| word | 意思 | Example sentence. |
"""
        
        # 构建用户提示词
        prompt = f"请用这些关键词创作一个有趣的英文故事：{keywords}"
        
        # 调用API生成故事
        response = get_claude_response(prompt, system_prompt)
        
        if response:
            # 显示生成的故事
            st.markdown("---")
            st.markdown(response)
            
            # 添加互动按钮
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("👍 很棒的故事！"):
                    st.success("谢谢你的喜欢！继续努力学习英语吧！")
            with col2:
                if st.button("📖 再来一个"):
                    st.info("修改关键词或点击'开始创作'按钮生成新故事！")
            with col3:
                if st.button("💾 收藏故事"):
                    st.info("故事已经显示在上方，你可以复制保存哦！")