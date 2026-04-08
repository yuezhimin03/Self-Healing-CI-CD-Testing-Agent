from fastapi import FastAPI, Request, BackgroundTasks
import uvicorn
# 硬核挂载：导入你之前写好的沙盒引擎
from sandbox import setup_and_run_sandbox

app = FastAPI()
def trigger_agent(repo_url, commit_sha):
    print(f"\n🚀 [中央大脑] 已接管云端崩溃任务！准备下发至隔离区...")

    # 核心闭环第一步：唤醒 Docker 沙盒拉取代码并重现报错
    returncode, error_log, workspace_dir = setup_and_run_sandbox(repo_url, commit_sha)

    if returncode != 0:
        print(f"\n🧠 [中央大脑] 沙盒已成功提取报错日志！准备呼叫 DeepSeek 算力集群进行代码自愈...")
        # （这是最后一步：我们马上会把 agent.py 里的修复逻辑接进这里，实现自动改代码）


@app.post("/webhook")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()

    if "workflow_run" in payload:
        status = payload["workflow_run"]["conclusion"]
        repo_name = payload["repository"]["full_name"]
        commit_sha = payload["workflow_run"]["head_sha"]

        # 动态拼接出 GitHub 仓库的真实物理下载链接
        repo_url = f"https://github.com/{repo_name}.git"

        if status == "failure":
            print(f"🚨 [网关] 警报！探测到 {repo_name} 流水线崩溃！")
            # 把耗时的拉代码和跑沙盒任务丢到后台执行
            background_tasks.add_task(trigger_agent, repo_url, commit_sha)

    return {"status": "received", "message": "Payload processed"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)