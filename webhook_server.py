from fastapi import FastAPI, Request, BackgroundTasks
import uvicorn

app = FastAPI()


def trigger_agent(repo_name, commit_sha):
    print(f"🚀 [网关] 正在唤醒智能体，准备接管 {repo_name} 的修复任务...")
    print(f"🔧 [网关] 锁定目标 Commit SHA {commit_sha}")
    # 这里是我们下一步（第二步）要接入 Docker 沙盒与 DeepSeek 推理引擎的接口
    # 目前先用日志占位，验证网络链路是否打通
    print(f"🧠 [网关] 沙盒环境准备完毕，等待注入出错代码...")


@app.post("/webhook")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    # 接收并解析来自 GitHub 的 JSON 数据包
    payload = await request.json()

    # 过滤出流水线运行事件
    if "workflow_run" in payload:
        status = payload["workflow_run"]["conclusion"]
        repo_name = payload["repository"]["full_name"]

        # 提取导致流水线崩溃的代码提交哈希值
        commit_sha = payload["workflow_run"]["head_sha"]

        if status == "failure":
            print(f"🚨 [网关] 探测到流水线崩溃！目标仓库 {repo_name}")
            # 将耗时的代码修复任务丢进后台线程，立即给 GitHub 返回 200 状态码，防止 Webhook 超时
            background_tasks.add_task(trigger_agent, repo_name, commit_sha)
        elif status == "success":
            print(f"✅ [网关] {repo_name} 流水线运行良好，智能体继续休眠。")

    return {"status": "received", "message": "Payload processed"}


if __name__ == "__main__":
    # 在本地 8000 端口启动高性能网关服务器
    uvicorn.run(app, host="0.0.0.0", port=8000)