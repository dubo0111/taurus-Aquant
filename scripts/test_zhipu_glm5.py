"""
测试智谱 AI GLM-5 模型
"""
import sys
from pathlib import Path
import os

# 加载 .env
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

env_file = project_root / ".env"
if env_file.exists():
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

print("=" * 60)
print("测试智谱 AI GLM-5")
print("=" * 60)

api_key = os.getenv('ZHIPU_API_KEY')
print(f"API Key: {api_key}")

try:
    from zhipuai import ZhipuAI

    client = ZhipuAI(api_key=api_key)
    print("✅ 客户端初始化成功\n")

    # 测试 GLM-5
    print("测试 GLM-5 模型:")
    print("-" * 60)

    response = client.chat.completions.create(
        model="glm-5",  # 使用 glm-5
        messages=[
            {"role": "user", "content": "你好"}
        ],
    )

    print(f"✅ 成功！")
    print(f"回复: {response.choices[0].message.content}")

    # 测试策略生成
    print("\n" + "=" * 60)
    print("测试策略生成:")
    print("-" * 60)

    response = client.chat.completions.create(
        model="glm-5",
        messages=[
            {
                "role": "system",
                "content": "你是一个量化交易策略开发者"
            },
            {
                "role": "user",
                "content": "用Python写一个简单的移动平均线策略，当快线上穿慢线时买入，"
            }
        ],
    )

    print(f"✅ 策略生成成功！")
    print(f"\n生成的代码：")
    print(response.choices[0].message.content)

    print("\n" + "=" * 60)
    print("🎉 GLM-5 测试完全成功！")
    print("=" * 60)

except Exception as e:
    print(f"\n❌ 失败: {e}")
    import traceback
    traceback.print_exc()
