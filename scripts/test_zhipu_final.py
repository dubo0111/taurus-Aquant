"""
测试智谱 AI - 使用正确的模型名称
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
print("测试智谱 AI API（修正版）")
print("=" * 60)

api_key = os.getenv('ZHIPU_API_KEY')
print(f"\n配置信息：")
print(f"  API Key: {api_key}")
print(f"  API Key 长度: {len(api_key) if api_key else 0}")

if not api_key:
    print("\n❌ ZHIPU_API_KEY 未配置")
    sys.exit(1)

try:
    from zhipuai import ZhipuAI

    print("\n" + "=" * 60)
    print("步骤 1: 初始化客户端")
    print("=" * 60)

    client = ZhipuAI(api_key=api_key)
    print("✅ 客户端初始化成功")

    # 测试可用的模型列表
    print("\n" + "=" * 60)
    print("步骤 2: 尝试不同的模型")
    print("=" * 60)

    models_to_try = ["glm-4", "glm-4-flash", "glm-3-turbo"]

    for model_name in models_to_try:
        print(f"\n尝试模型: {model_name}")

        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "user", "content": "你好"}
                ],
            )

            print(f"✅ 模型 {model_name} 可用")
            print(f"  回复: {response.choices[0].message.content}")

            # 如果成功，保存可用的模型名称
            print(f"\n✅ 找到可用模型: {model_name}")
            print(f"\n建议在 .env 中设置: ZHIPU_MODEL={model_name}")

            break

        except Exception as e:
            print(f"❌ 模型 {model_name} 失败: {str(e)[:100]}")
            continue

    print("\n" + "=" * 60)
    print("🎉 测试完成")
    print("=" * 60)

except Exception as e:
    print(f"\n❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
