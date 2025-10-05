@echo off
chcp 65001 > nul
echo 🏠 启动克劳德的奇妙英语屋...
echo ================================

REM 检查Python是否安装
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: Python未安装
    echo 请先安装Python 3.8或更高版本
    pause
    exit /b 1
)

REM 检查并安装依赖
echo 📦 检查依赖...
pip install -q -r requirements.txt

REM 检查streamlit是否安装成功
streamlit --version > nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: Streamlit安装失败
    echo 请手动运行: pip install -r requirements.txt
    pause
    exit /b 1
)

echo ✅ 依赖检查完成
echo ================================
echo 🚀 正在启动应用...
echo 应用将在浏览器中打开: http://localhost:8501
echo 按 Ctrl+C 停止应用
echo ================================

REM 启动Streamlit应用
streamlit run app.py