# 🏠 克劳德的奇妙英语屋
Claude's English Fun House - 让英语学习充满乐趣！

## 📖 项目介绍

克劳德的奇妙英语屋是一个专为10-12岁中国小学生设计的交互式英语学习应用。通过强大的AI技术，我们将枯燥的英语学习变成有趣的冒险之旅！

### ✨ 核心功能

1. **📖 AI故事魔法屋** - 输入关键词，AI为你创作独一无二的英文故事
2. **🗣️ 角色扮演聊天室** - 和有趣的角色用英语对话，提高口语表达能力
3. **🖋️ 我是小作家** - 写英文作品，AI老师给你贴心的批改和建议

## 🚀 快速开始

### 环境要求

- Python 3.8 或更高版本
- 稳定的网络连接
- API密钥（支持OpenAI协议的API服务）

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/yourusername/english-fun-house.git
cd english-fun-house
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置API（可选）**

如果你想使用环境变量配置，可以创建 `.env` 文件：
```bash
cp .env.example .env
```

然后编辑 `.env` 文件，填入你的API配置：
```
OPENAI_API_KEY=your_api_key_here
OPENAI_API_BASE=https://your-api-endpoint.com/v1  # 可选
OPENAI_MODEL=your-model-name  # 可选
```

4. **启动应用**
```bash
streamlit run app.py
```

应用会在浏览器中自动打开，默认地址是 `http://localhost:8501`

## 📱 使用指南

### 第一步：连接API

1. 在左侧侧边栏找到"API配置"部分
2. 输入你的API密钥
3. （可选）点击"高级配置"设置自定义端点和模型
4. 点击"连接API"按钮
5. 看到"✅ API连接成功！"表示配置完成

### 第二步：选择功能

在侧边栏选择你想使用的功能：

#### 📖 AI故事魔法屋
- 输入1-3个英文关键词（用逗号分隔）
- 点击"开始创作"
- AI会生成包含这些关键词的有趣故事
- 故事后面还有重点词汇表，帮助你学习新单词

#### 🗣️ 角色扮演聊天室
- 选择一个你喜欢的角色
- 在聊天框中输入英文消息
- 角色会用英语回复你
- 可以随时切换角色或开始新对话

#### 🖋️ 我是小作家
- 在文本框中写下你的英文作品
- 点击"请老师批改"
- AI老师会给出详细的批改建议
- 包括总体评价、修改建议和新知识点

## 🎯 学习小贴士

1. **每天坚持使用** - 每天花15-30分钟使用应用，进步会很明显
2. **大胆尝试** - 不要害怕犯错，错误是学习的一部分
3. **记录进步** - 保存你喜欢的故事和批改结果，看看自己的进步
4. **享受过程** - 学习应该是快乐的，享受与AI互动的每一刻

## 🛠️ 技术架构

```
english-fun-house/
├── app.py                 # 主应用程序
├── requirements.txt       # 项目依赖
├── .env.example          # 环境变量示例
├── config/
│   └── settings.py       # 配置管理
├── modules/
│   ├── __init__.py
│   ├── story_magic.py    # AI故事魔法屋模块
│   ├── role_chat.py      # 角色扮演聊天室模块
│   └── little_writer.py  # 我是小作家模块
└── utils/
    └── api_client.py     # API客户端管理
```

## 🔧 配置说明

### API配置选项

- **API密钥** (必需): 你的API服务密钥
- **API端点** (可选): 自定义API端点URL，默认为OpenAI官方端点
- **模型名称** (可选): 指定使用的模型，默认为 `claude-3-opus-20240229`

### 支持的API服务

本应用支持所有兼容OpenAI协议的API服务，包括：
- OpenAI官方API
- Azure OpenAI Service
- AWS Bedrock (通过OpenAI协议封装)
- 其他兼容OpenAI协议的第三方服务

## 📊 功能特点

| 功能 | 特点 | 适合场景 |
|------|------|---------|
| AI故事魔法屋 | 个性化故事生成、词汇学习 | 扩展词汇量、阅读理解 |
| 角色扮演聊天室 | 实时对话、多角色选择 | 口语练习、日常对话 |
| 我是小作家 | 详细批改、鼓励式反馈 | 写作练习、语法提升 |

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork 本项目
2. 创建你的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 📝 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- 感谢所有为这个项目贡献代码的开发者
- 感谢Streamlit提供优秀的Web框架
- 感谢OpenAI/Anthropic提供强大的AI能力

## 📧 联系我们

如有问题或建议，请通过以下方式联系：

- 提交 [Issue](https://github.com/yourusername/english-fun-house/issues)
- 发送邮件至: your-email@example.com

---

**让我们一起在克劳德的奇妙英语屋中快乐学习英语吧！** 🎉

Made with ❤️ for young English learners