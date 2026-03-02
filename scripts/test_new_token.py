"""
测试新的 Tushare Token
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import tushare as ts
import tushare.pro.client as client

# 从 .env 读取配置
from src.utils.config import settings

print("=" * 60)
print("测试 Tushare Token（新）")
print("=" * 60)

print(f"Token: {settings.TUSHARE_TOKEN[:10]}...")
print(f"API URL: {settings.TUSHARE_API_URL}")

try:
    # 设置自定义 API URL
    if settings.TUSHARE_API_URL:
        client.DataApi._DataApi__http_url = settings.TUSHARE_API_URL
        print(f"✅ 设置自定义 API URL: {settings.TUSHARE_API_URL}")

    # 初始化 pro_api
    pro = ts.pro_api(settings.TUSHARE_TOKEN)
    print("✅ pro_api 初始化成功")

    # 测试1：获取交易日历
    print("\n" + "=" * 60)
    print("测试1：获取交易日历")
    print("=" * 60)
    df = pro.trade_cal(exchange='SSE', start_date='20260101', end_date='20260110')
    print(f"✅ 成功获取 {len(df)} 条交易日历数据")
    print(df.head())

    # 测试2：获取日线数据
    print("\n" + "=" * 60)
    print("测试2：获取日线数据（平安银行 000001.SZ）")
    print("=" * 60)
    df = pro.daily(ts_code='000001.SZ', start_date='20260101', end_date='20260228')
    print(f"✅ 成功获取 {len(df)} 条日线数据")
    print(df.head())

    # 测试3：获取股票列表
    print("\n" + "=" * 60)
    print("测试3：获取股票列表")
    print("=" * 60)
    df = pro.stock_basic(exchange='SSE', list_status='L', limit=10)
    print(f"✅ 成功获取 {len(df)} 只股票")
    print(df.head())

    # 测试4：用户提供的示例
    print("\n" + "=" * 60)
    print("测试4：用户提供的示例")
    print("=" * 60)
    df = pro.daily_basic(**{"limit": 20}, fields=["ts_code", "trade_date", "close", "pb", "ps"])
    print(f"✅ 成功获取 {len(df)} 条数据")
    print(df)

    print("\n" + "=" * 60)
    print("🎉 所有测试通过！Token 有效！")
    print("=" * 60)

except Exception as e:
    print(f"\n❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
