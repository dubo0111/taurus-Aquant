"""
测试智谱 AI API
"""
import sys
from pathlib import Path
import os

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 加载 .env 文件
env_file = project_root / ".env"
if env_file.exists():
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

print("=" * 60)
print("测试智谱 AI API")
print("=" * 60)

print(f"\n配置信息：")
print(f"  ZHIPU_API_KEY: {os.getenv('ZHIPU_API_KEY', 'NOT SET')[:20]}...")
print(f"  ZHIPU_MODEL: {os.getenv('ZHIPU_MODEL', 'NOT SET')}")

try:
    from zhipuai import ZhipuAI

    print("\n初始化智谱 AI 客户端...")
    client = ZhipuAI(api_key=os.getenv('ZHIPU_API_KEY'))

    print(f"✅ 客户端初始化成功")

    # 测试1：简单对话
    print("\n" + "=" * 60)
    print("测试1：简单对话")
    print("=" * 60)

    response = client.chat.completions.create(
        model=os.getenv('ZHIPU_MODEL', 'glm-5'),
        messages=[
            {"role": "user", "content": "你好，请用一句话介绍量化交易"}
        ],
        temperature=0.7,
        max_tokens=200
    )

    print(f"✅ 对话成功")
    print(f"\n回复内容：")
    print(response.choices[0].message.content)

    # 测试2：生成策略代码
    print("\n" + "=" * 60)
    print("测试2：生成策略代码")
    print("=" * 60)

    response = client.chat.completions.create(
        model=os.getenv('ZHIPU_MODEL', 'glm-5'),
        messages=[
            {
                "role": "system",
                "content": "你是一个专业的量化交易策略开发者。请根据用户需求生成Python代码。"
            },
            {
                "role": "user",
                "content": "生成一个简单的移动平均线策略代码，当快线上穿慢线时买入，下穿时卖出。"
            }
        ],
        temperature=0.7,
        max_tokens=500
    )

    print(f"✅ 代码生成成功")
    print(f"\n生成的代码：")
    print(response.choices[0].message.content)

    print("\n" + "=" * 60)
    print("🎉 智谱 AI API 测试成功！")
    print("=" * 60)

except Exception as e:
    print(f"\n❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
