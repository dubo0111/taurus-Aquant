"""
测试智谱 AI Agent 服务
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 加载 .env
import os
env_file = project_root / ".env"
if env_file.exists():
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

print("=" * 60)
print("测试智谱 AI Agent 服务")
print("=" * 60)

try:
    from src.agent.agent_service import ZhipuAgent
    from src.utils.config import settings

    print(f"\n配置信息：")
    print(f"  API Key: {settings.ZHIPU_API_KEY[:20]}...")
    print(f"  Model: {settings.ZHIPU_MODEL}")

    # 初始化 Agent
    print("\n" + "=" * 60)
    print("步骤 1: 初始化 Agent")
    print("=" * 60)

    agent = ZhipuAgent()
    print("✅ Agent 初始化成功")

    # 测试 1：简单对话
    print("\n" + "=" * 60)
    print("测试 1: 简单对话")
    print("=" * 60)

    messages = [{"role": "user", "content": "你好，请用一句话介绍量化交易"}]
    response = agent.chat(messages)
    print(f"✅ 对话成功")
    print(f"\n回复：{response}")

    # 测试 2：生成策略
    print("\n" + "=" * 60)
    print("测试 2: 生成策略代码")
    print("=" * 60)

    result = agent.generate_strategy("生成一个基于RSI指标的交易策略")
    print(f"✅ 策略生成成功")
    print(f"\n代码：\n{result['code'][:500]}...")

    # 测试 3：解释指标
    print("\n" + "=" * 60)
    print("测试 3: 解释技术指标")
    print("=" * 60)

    explanation = agent.explain_indicator("MACD")
    print(f"✅ 指标解释成功")
    print(f"\n{explanation[:300]}...")

    print("\n" + "=" * 60)
    print("🎉 所有 Agent 测试通过！")
    print("=" * 60)

except Exception as e:
    print(f"\n❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
