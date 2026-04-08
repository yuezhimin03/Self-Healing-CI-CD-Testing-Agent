import os
import re
from openai import OpenAI
import subprocess

# 初始化 DeepSeek 客户端
client = OpenAI(
    api_key="sk-759ae72757d74a5390958b935656a9cf",  # <--- 换成你自己的 Key！
    base_url="https://api.deepseek.com"
)


def auto_fix_code(error_log):
    print("\n🧠 [大模型引擎] 正在分析崩溃日志并定位代码裂痕...")

    # 锁定我们需要修复的目标文件
    target_file = "calculator.py"

    with open(target_file, "r", encoding="utf-8") as f:
        source_code = f.read()

    prompt = f"""
    你是一个无情的自动化测试与修复大模型。
    你的任务是修复下面这段报错的 Python 代码。

    【原始代码】
    {source_code}

    【沙盒捕获的堆栈报错】
    {error_log}

    请直接输出修复后的完整 Python 代码。
    要求：
    1. 绝对不要包含任何解释、寒暄或注释。
    2. 绝对不要使用 Markdown 代码块符号 (例如 ```python) 包裹代码。
    3. 你输出的内容必须可以直接被机器保存为 .py 文件运行。
    """

    print("🚀 [大模型引擎] 正在向 DeepSeek 算力集群请求修复补丁...")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个纯粹的代码生成机器，没有情感，只有逻辑。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )

    fixed_code = response.choices[0].message.content.strip()

    # 底层暴力清洗：防止大模型偶尔不听话乱加 Markdown 符号
    fixed_code = re.sub(r"^```python\n?", "", fixed_code)
    fixed_code = re.sub(r"^```\n?", "", fixed_code)
    fixed_code = re.sub(r"```$", "", fixed_code)

    print("💉 [大模型引擎] 补丁获取成功！正在向本地物理硬盘注入无菌代码...")
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(fixed_code)

    print("✅ [大模型引擎] 本地文件覆写完毕！准备接管 Git 发射程序...")

    # 机器接管：自动提交并推送到云端
    subprocess.run(["git", "add", target_file])
    subprocess.run(["git", "commit", "-m", "fix: auto-healed by DeepSeek Agent"])
    subprocess.run(["git", "push", "origin", "HEAD"])
    print("🎉 [系统通告] 修复补丁已由智能体自动发射升空！系统闭环自愈完成！")