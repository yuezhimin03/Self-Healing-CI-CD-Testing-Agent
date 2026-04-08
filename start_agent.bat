@echo off
echo 🚀 [系统指挥舱] 正在为您唤醒全自动自愈型 CI/CD 智能体...
echo.

REM 第一级推进器：呼叫独立的终端窗口启动 Ngrok 物理隧道
echo 📡 正在点火 Ngrok 雷达...
start "Ngrok Radar" cmd /k ".\ngrok http 8000"

REM 第二级推进器：呼叫独立的终端窗口，激活虚拟环境并启动网关大脑
echo 🧠 正在点火 Python 中央大脑...
start "Central Brain" cmd /k "call .venv\Scripts\activate && python webhook_server.py"

echo.
echo ✅ [系统指挥舱] 基础设施全线就绪！
echo ⚠️ 终极操作指南
echo 1. 请在弹出的 Ngrok 窗口中复制最新的 https 链接
echo 2. 前往 GitHub Webhooks 设置页替换旧链接（切记末尾加上 /webhook）
echo 3. 开始你的代码创作
echo.
pause