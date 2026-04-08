import subprocess
import os
import tempfile


def setup_and_run_sandbox(repo_url, commit_sha):
    """在 Docker 隔离沙盒中拉取代码并运行测试"""
    print(f"\n📦 [沙盒] 正在为 {repo_url} 创建无菌隔离环境...")

    # 动态分配临时手术台
    temp_dir = tempfile.mkdtemp(prefix="agent_workspace_")
    print(f"📂 [沙盒] 临时物理工作目录已创建: {temp_dir}")

    try:
        # 从云端拉取指定版本的出错代码
        print(f"⬇️ [沙盒] 正在执行 Git Clone 拉取云端代码...")
        subprocess.run(["git", "clone", repo_url, temp_dir], check=True, capture_output=True)

        # 精准切换到触发报错的那次 Commit 节点
        print(f"🎯 [沙盒] 正在锁定目标快照: {commit_sha[:7]}")
        subprocess.run(["git", "-C", temp_dir, "checkout", commit_sha], check=True, capture_output=True)

        # ==========================================
        # 这里就是你问的“Docker 代码”核心区域！
        # ==========================================
        print("🐳 [沙盒] 正在启动 Docker 容器执行隔离区测试...")
        docker_cmd = [
            "docker", "run", "--rm",
            "-v", f"{temp_dir}:/app",  # 将本地临时代码目录挂载到容器内
            "-w", "/app",  # 设置容器的工作目录
            "python:3.12-slim",  # 直接拉取云端极其轻量的 Python 纯净镜像
            "sh", "-c", "pip install pytest -q && pytest"  # 注入底层的测试指令
        ]

        # 执行容器指令并捕获全量日志
        result = subprocess.run(docker_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")

        returncode = result.returncode
        output = result.stdout + result.stderr

        if returncode != 0:
            print("❌ [沙盒] 隔离区测试失败！已成功捕获报错堆栈。")
        else:
            print("✅ [沙盒] 隔离区测试通过，代码状态健康。")

        return returncode, output, temp_dir

    except Exception as e:
        print(f"⚠️ [沙盒] 基础设施崩溃，执行流中断: {str(e)}")
        return 1, str(e), temp_dir