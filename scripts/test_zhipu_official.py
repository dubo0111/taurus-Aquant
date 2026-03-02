"""
测试智谱 AI API - 官方示例
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
print("测试智谱 AI API（官方示例）")
print("=" * 60)

api_key = os.getenv('ZHIPU_API_KEY')
model = os.getenv('ZHIPU_MODEL', 'glm-4')  # 默认使用 glm-4

print(f"\n配置信息：")
print(f"  API Key: {api_key}")
print(f"  Model: {model}")
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

    print("\n" + "=" * 60)
    print("步骤 2: 测试简单对话（官方示例）")
    print("=" * 60)

    # 使用官方文档的示例
    response = client.chat.completions.create(
        model="glm-4",  # 使用 glm-4 而不是 glm-5
        messages=[
            {"role": "user", "content": "你好"}
        ],
    )

    print(f"✅ 对话成功")
    print(f"\n返回数据：")
    print(f"  ID: {response.id}")
    print(f"  Model: {response.model}")
    print(f"  Content: {response.choices[0].message.content}")

    print("\n" + "=" * 60)
    print("步骤 3: 测试策略生成")
    print("=" * 60)

    response = client.chat.completions.create(
        model="glm-4",
        messages=[
            {"role": "system", "content": "你是一个量化交易策略开发者"},
            {"role": "user", "content": "用一句话介绍双均线策略"}
        ],
    )

    print(f"✅ 策略生成成功")
    print(f"\n回复：{response.choices[0].message.content}")

    print("\n" + "=" * 60)
    print("🎉 智谱 AI API 测试完全成功！")
    print("=" * 60)

except Exception as e:
    print(f"\n❌ 测试失败: {e}")
    print(f"\n错误类型: {type(e).__name__}")

    import traceback
    print("\n详细错误信息：")
    traceback.print_exc()

    print("\n" + "=" * 60)
    print("💡 可能的解决方案：")
    print("=" * 60)
    print("1. 检查 API Key 是否正确")
    print("2. 检查账户余额")
    print("3. 尝试使用 glm-4 模型（而不是 glm-5）")
    print("4. 访问 https://open.bigmodel.cn/ 查看账户状态")

    sys.exit(1)
