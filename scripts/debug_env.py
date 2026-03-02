"""
调试 Tushare 连接 - 简化版
"""
import sys
from pathlib import Path
import os

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 先手动加载 .env 文件
print("=" * 60)
print("手动加载 .env 文件")
print("=" * 60)

env_file = project_root / ".env"
print(f"查找 .env 文件: {env_file}")
print(f".env 文件存在: {env_file.exists()}")

if env_file.exists():
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                os.environ[key] = value
                if 'TUSHARE' in key or 'ZHIPU' in key:
                    print(f"  {key}: {value[:20]}...")

print("\n环境变量检查：")
print(f"  TUSHARE_TOKEN: {os.getenv('TUSHARE_TOKEN', 'NOT SET')[:20]}...")
print(f"  TUSHARE_API_URL: {os.getenv('TUSHARE_API_URL', 'NOT SET')}")

# 现在测试
print("\n" + "=" * 60)
print("测试 Tushare API")
print("=" * 60)

import tushare as ts
import tushare.pro.client as client

try:
    # 设置 API URL
    api_url = os.getenv('TUSHARE_API_URL')
    if api_url:
        client.DataApi._DataApi__http_url = api_url
        print(f"✅ 设置 API URL: {api_url}")

    # 创建 pro_api
    token = os.getenv('TUSHARE_TOKEN')
    print(f"✅ 使用 Token: {token[:20]}...")

    pro = ts.pro_api(token)

    # 测试调用
    df = pro.daily_basic(**{"limit": 5}, fields=["ts_code", "trade_date", "close"])
    print(f"\n✅ 成功获取 {len(df)} 条数据")
    print(df)

    print("\n" + "=" * 60)
    print("🎉 Tushare API 测试成功！")
    print("=" * 60)

except Exception as e:
    print(f"\n❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
