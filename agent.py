import subprocess
import os
import re
from openai import OpenAI

# 接入 DeepSeek 的核心网关（直接硬编码你的密钥，暴力绕过系统的环境变量限制）
client = OpenAI(
    api_key="sk-759ae72757d74a5390958b935656a9cf",
    base_url="https://api.deepseek.com"
)

TARGET_FILE = "calculator.py"
TEST_CMD = ["pytest", "test_calculator.py"]


def run_tests():
    """运行测试并捕获输出"""
    print("🚀 [Agent] 正在执行测试流水线...")
    # 解决 Windows 终端 GBK 编码冲突，强制使用 utf-8 并容错替换乱码字符
    result = subprocess.run(TEST_CMD, capture_output=True, encoding="utf-8", errors="replace")

    # 增加类型安全防御机制，防止输出流截断返回 None
    stdout = result.stdout if result.stdout else ""
    stderr = result.stderr if result.stderr else ""

    return result.returncode, stdout + stderr


def read_source_code():
    """读取当前出错的源代码"""
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        return f.read()


def write_source_code(new_code):
    """将修复后的代码覆盖写入文件"""
    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(new_code)
    print(f"🔧 [Agent] 已成功将修复代码写入 {TARGET_FILE}")


def heal_code(error_log, current_code):
    """调用 DeepSeek 大模型进行代码诊断和修复"""
    print("🧠 [Agent] 发现错误，正在呼叫 DeepSeek 算力集群进行修复诊断...")

    prompt = f"""
    你是一个世界顶级的 Python 工程师。现在的任务是修复出错的代码。

    【当前源代码】
    ```python
    {current_code}
    ```

    【测试报错日志】
    {error_log}

    请分析报错原因，并给出修复后的完整代码。
    要求
    1. 必须输出完整的 {TARGET_FILE} 代码，不能省略。
    2. 只输出代码，必须包裹在 ```python 和 ``` 之间，不要任何多余的解释废话。
    """

    response = client.chat.completions.create(
        model="deepseek-coder",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    reply = response.choices[0].message.content

    # 使用正则提取包裹在 Markdown 代码块中的纯代码
    match = re.search(r'```python\n(.*?)\n```', reply, re.DOTALL)
    if match:
        return match.group(1)
    else:
        # 容错处理
        return reply.replace('```python', '').replace('```', '').strip()


def main():
    max_retries = 3
    attempt = 1

    while attempt <= max_retries:
        print(f"\n--- 尝试回合 {attempt}/{max_retries} ---")
        returncode, output = run_tests()

        if returncode == 0:
            print("✅ [Agent] 测试全部通过！代码处于完美状态。")
            break

        print("❌ [Agent] 测试失败，准备介入修复。")
        current_code = read_source_code()

        # 核心逻辑
        fixed_code = heal_code(output, current_code)
        write_source_code(fixed_code)

        attempt += 1

    if attempt > max_retries:
        print("⚠️ [Agent] 达到最大重试次数，修复失败，请人类工程师介入。")


if __name__ == "__main__":
    main()