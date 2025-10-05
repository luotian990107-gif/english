"""
配置管理模块
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# API配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "claude-3-opus-20240229")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "15000"))  # Gemini-2.5-pro 支持的最大token数
TEMPERATURE = 0.7

# UI配置
APP_TITLE = "🏠 克劳德的奇妙英语屋"
APP_SUBTITLE = "Claude's English Fun House"
APP_DESCRIPTION = """
欢迎来到克劳德的奇妙英语屋！这里有三个超级有趣的英语学习功能：

📖 **AI故事魔法屋** - 输入关键词，AI为你创作精彩故事  
🗣️ **角色扮演聊天室** - 和有趣的角色用英语对话  
🖋️ **我是小作家** - 写英文，AI老师给你贴心批改  

让我们一起快乐学英语吧！
"""

# 功能模块配置
MODULES = {
    "story": "📖 AI故事魔法屋",
    "chat": "🗣️ 角色扮演聊天室",
    "writer": "🖋️ 我是小作家"
}

# 角色扮演角色列表
CHAT_ROLES = [
    "🛸 一个友好的外星人",
    "🦸 美国队长",
    "🐱 一只会说话的猫",
    "🧙‍♂️ 霍格沃茨的魔法老师",
    "🤖 来自未来的机器人",
    "🦖 一只可爱的恐龙",
    "👨‍🚀 国际空间站的宇航员",
    "🧚 森林里的小精灵"
]

# 故事默认关键词
DEFAULT_KEYWORDS = "dragon, castle, magic"

# 作文默认示例
DEFAULT_WRITING_SAMPLE = """I go to school every day. My favorite subject is English. I like read books and play games. Yesterday I go to the park with my friend. We are very happy!"""