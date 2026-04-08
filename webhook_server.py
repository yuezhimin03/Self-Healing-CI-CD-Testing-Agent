from fastapi import FastAPI, Request, BackgroundTasks
import uvicorn
from sandbox import setup_and_run_sandbox
from agent import auto_fix_code  # <--- 导入你的大模型大脑

app = FastAPI()


def trigger_agent(repo_url, commit_sha):
    print(f"\n🚀 [中央大脑] 已接管云端崩溃任务！准备下发至隔离区...")

    # 1. 唤醒 Docker 沙盒拉取代码并重现报错
    returncode, error_log, workspace_dir = setup_and_run_sandbox(repo_url, commit_sha)

    if returncode != 0:
        print(f"\n🚨 [中央大脑] 隔离区证实代码存在致命缺陷。进入二阶自愈模式...")
        # 2. 呼叫大模型进行代码覆写与自动推送
        auto_fix_code(error_log)


@app.post("/webhook")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()
    if "workflow_run" in payload:
        status = payload["workflow_run"]["conclusion"]
        repo_name = payload["repository"]["full_name"]
        commit_sha = payload["workflow_run"]["head_sha"]
        repo_url = f"https://github.com/{repo_name}.git"

        if status == "failure":
            print(f"🚨 [网关] 警报！探测到 {repo_name} 流水线崩溃！")
            background_tasks.add_task(trigger_agent, repo_url, commit_sha)

    return {"status": "received"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)