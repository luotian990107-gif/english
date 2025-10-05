# 🚀 快速启动指南

## 立即运行（已配置好API）

你的API配置已经设置完成！现在可以直接运行应用：

### 方法1：使用启动脚本（推荐）

**Mac/Linux用户：**
```bash
./启动.sh
```

**Windows用户：**
```bash
run.bat
```

### 方法2：直接运行Streamlit

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
streamlit run app.py
```

应用将在浏览器中自动打开：http://localhost:8501

## 📝 使用步骤

1. **应用启动后**，你会看到主界面

2. **在左侧侧边栏**：
   - API密钥已经预配置（从.env文件读取）
   - 点击 "🔗 连接API" 按钮激活连接
   - 你应该会看到 "✅ API连接成功！"

3. **选择功能**：
   - 📖 AI故事魔法屋 - 创作英文故事
   - 🗣️ 角色扮演聊天室 - 英语对话练习
   - 🖋️ 我是小作家 - 英文写作批改

## 🔧 API配置信息

当前配置（已保存在 `.env` 文件中）：
- **API密钥**: sk-eem5wOJlaV6JG9CTT7LTAAruET6OZnrj0Jsf0Jgy6EZAReSn
- **API端点**: https://bmc-llm-relay.bluemediagroup.cn/v1
- **模型**: gemini-2.5-pro
- **最大Token数**: 15000

如果需要修改配置，可以：
1. 编辑 `.env` 文件
2. 或在应用界面的侧边栏中直接修改

## 📁 项目结构（已优化）

```
english/
├── .env                      # 你的API配置
├── .env.example             # 配置示例
├── .gitignore              # Git忽略
├── app.py                  # 主应用
├── requirements.txt        # 依赖（只需3个包）
├── README.md              # 项目文档
├── QUICK_START.md         # 本文档
├── 启动.sh                # Mac/Linux启动脚本
├── run.bat                # Windows启动脚本
├── config/
│   └── settings.py        # 配置管理
├── modules/               # 功能模块
│   ├── __init__.py
│   ├── story_magic.py     # AI故事魔法屋
│   ├── role_chat.py       # 角色扮演聊天室
│   └── little_writer.py   # 我是小作家
└── utils/
    └── api_client_simple.py  # 简化的API客户端
```

## ⚠️ 注意事项

1. **首次运行**需要安装3个依赖包：streamlit, requests, python-dotenv
2. **确保网络连接**稳定，因为需要调用远程API
3. **API调用**可能会产生费用，请注意使用量

## 🆘 常见问题

### Q: 应用无法启动？
A: 确保已安装Python 3.8+，运行 `pip install -r requirements.txt` 安装依赖

### Q: API连接失败？
A: 检查网络连接，确保能访问 https://bmc-llm-relay.bluemediagroup.cn

### Q: 出现"proxies"错误？
A: 这个问题已修复！我们使用了简化的API客户端，避免了OpenAI SDK的兼容性问题

## 📊 测试建议

建议按以下顺序测试各个功能：

1. **AI故事魔法屋**
   - 输入关键词：`cat, moon, adventure`
   - 点击"开始创作"
   - 查看生成的故事和词汇表

2. **角色扮演聊天室**
   - 选择"🐱 一只会说话的猫"
   - 输入：`Hello! What's your name?`
   - 进行几轮对话

3. **我是小作家**
   - 输入示例文本：`Today I go to school. I like my teacher. She is very kind.`
   - 点击"请老师批改"
   - 查看批改结果

## 🎉 开始使用

现在一切准备就绪！运行应用，开始愉快的英语学习之旅吧！

如有任何问题，请查看主 README.md 文档。

---
✨ **项目已优化完成**
- ✅ 修复了所有兼容性问题
- ✅ 清理了冗余文件（从23个减少到17个）
- ✅ 使用简化的API客户端
- ✅ 只需3个Python包依赖