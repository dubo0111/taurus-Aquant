"""
使用官方示例测试智谱 AI GLM-5
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
print("测试智谱 AI GLM-5（官方示例）")
print("=" * 60)

# 获取 API Key
api_key = os.getenv('ZHIPU_API_KEY')
print(f"API Key: {api_key}")

try:
    from zhipuai import ZhipuAI

    print("\n初始化客户端...")
    client = ZhipuAI(api_key=api_key)
    print("✅ 客户端初始化成功")

    print("\n调用 GLM-5 模型...")
    response = client.chat.completions.create(
        model="glm-5",
        messages=[
            {"role": "user", "content": "Hello, ZhipuAI!"}
        ]
    )

    print("✅ 调用成功！")
    print(f"\n回复内容：")
    print(response.choices[0].message.content)

    print("\n" + "=" * 60)
    print("🎉 GLM-5 测试成功！")
    print("=" * 60)

except Exception as e:
    print(f"\n❌ 失败: {e}")

    error_msg = str(e)
    if "余额不足" in error_msg or "429" in error_msg:
        print("\n💡 余额问题，尝试使用 glm-4-flash...")
        try:
            response = client.chat.completions.create(
                model="glm-4-flash",
                messages=[
                    {"role": "user", "content": "Hello, ZhipuAI!"}
                ]
            )
            print("✅ glm-4-flash 可用！")
            print(f"\n回复：{response.choices[0].message.content}")

            print("\n" + "=" * 60)
            print("💡 建议使用 glm-4-flash（免费）")
            print("修改 .env: ZHIPU_MODEL=glm-4-flash")
            print("=" * 60)
        except Exception as e2:
            print(f"❌ glm-4-flash 也失败: {e2}")

    import traceback
    traceback.print_exc()
