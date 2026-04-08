🤖 自愈型持续集成与测试智能体 (Self-Healing CI/CD Agent)

架构愿景 | Vision

传统的 CI/CD 流水线在遇到错误时只会亮起红灯并等待人类工程师介入。本项目基于第一性原理重构了持续集成工作流，构建了一个真正意义上的闭环全自动数字员工。

当云端代码测试崩溃时，系统将自动穿透物理网络将错误栈拉回本地，在 Docker 无菌沙盒中进行复现，并直接调度大语言模型（DeepSeek/ChatGpt ）算力集群分析逻辑裂痕。AI 将自主生成补丁，甚至接管本地物理硬盘进行代码覆写，最终自动完成 Git 推送。

人类工程师只需专注创造，机器的错误交由机器自愈。

⚙️ 核心架构 | Architecture
系统分为四大物理与逻辑模块：

第一级探测器 (Cloud CI)：依托 GitHub Actions 进行自动化测试，崩溃时向网关发射 Webhook 信号。

第二级雷达 (Gateway)：基于 FastAPI + Ngrok 构建的本地监听站，负责跨越防火墙捕获云端报警。

第三级隔离舱 (Sandbox)：动态拉起的 Docker 容器，作为绝对安全的无菌室重现崩溃日志。

超级大脑 (AI Agent)：DeepSeek 神经网络直接接管文件系统，输出无菌代码并执行版本控制发射序列。

graph TD

    A[👨‍💻 开发者提交代码] -->|Git Push| B(☁️ GitHub Actions流水线)
    
    B -->|测试通过 ✅| C[🎉 部署成功]
    
    B -->|测试失败 ❌| D(📡 发送 Webhook 报警)
    
    D -->|Ngrok 物理隧道| E[💻 本地 FastAPI 网关]
    
    E -->|调度| F[🐳 Docker 隔离沙盒复现错误]
    
    F -->|提取错误日志| G[🧠 DeepSeek 大模型大脑]
    
    G -->|生成修复代码| H[💾 本地文件覆写]
    
    H -->|接管版本控制| I[🚀 自动 Git Commit & Push]
    
    I -->|触发新一轮测试| B

    🛠️ 装备清单 | Tech Stack
    
核心调度: Python 3.12

网关雷达: FastAPI, Uvicorn

内网穿透: Ngrok

隔离环境: Docker

神经引擎: OpenAI SDK (DeepSeek API)

云端基建: GitHub Actions

🚀 启动序列 | Getting Started
1. 物理环境配置
   
请确保你的计算机已安装 Git、Python 和 Docker Desktop（需保持运行状态）。

克隆本仓库并装填依赖弹药：

git clone https://github.com/yuezhimin03/Self-Healing-CI-CD-Testing-Agent.git

cd Self-Healing-CI-CD-Testing-Agent

python -m venv .venv

.venv\Scripts\activate  # Windows 激活虚拟环境 (Mac/Linux 使用 source .venv/bin/activate)

pip install -r requirements.txt

2. 注入神经密钥 (Security First)
   
绝对禁止将明文 Key 写入代码！ 在系统环境变量中设置你的 DeepSeek API 密钥：

Windows (CMD): setx DEEPSEEK_API_KEY "sk-你的真实密钥"

Mac/Linux: export DEEPSEEK_API_KEY="sk-你的真实密钥"

3. 一键点火 (Ignition)
   
Windows 用户可直接双击项目根目录下的 start_agent.bat。

系统将自动分裂出两个指挥舱：

Ngrok 隧道：负责建立跨墙连接。

FastAPI 网关：负责监听云端报警。

4. 对齐物理坐标
   
在弹出的 Ngrok 终端中，复制 Forwarding 后面的 https://... 链接。

进入本项目的 GitHub 仓库 -> Settings -> Webhooks。

将链接粘贴至 Payload URL，并务必在末尾加上 /webhook。


Content type 选择 application/json，保存更新。
<img width="1600" height="860" alt="a65b20c84d3539be69c797e3191e0ef4" src="https://github.com/user-attachments/assets/5e9cafee-b5c9-49cb-86b9-942ea5e812a7" />
