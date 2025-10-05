#!/bin/bash

echo "🏠 克劳德的奇妙英语屋 - 快速启动"
echo "==========================================="

# 检查Python
echo "📦 检查Python环境..."
python3 --version

# 安装依赖
echo "📦 安装必要的依赖..."
pip3 install -q requests streamlit python-dotenv

# 测试API连接
echo ""
echo "🔧 测试API连接..."
python3 test_simple_client.py

echo ""
echo "==========================================="
read -p "按Enter键启动应用，或按Ctrl+C退出..."

# 启动应用
echo "🚀 启动应用..."
echo "应用地址: http://localhost:8501"
echo "按 Ctrl+C 停止应用"
echo "==========================================="

streamlit run app.py