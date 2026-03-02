"""
强制测试 Tushare 适配器
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data.adapters.tushare_adapter import TushareAdapter
from src.utils.config import settings


def test_tushare_adapter():
    """测试 Tushare 适配器"""
    print("=" * 60)
    print("测试 Tushare 适配器（第三方镜像）")
    print("=" * 60)
    print(f"Token: {settings.TUSHARE_TOKEN[:10]}...")
    print(f"API URL: {settings.TUSHARE_API_URL}")

    try:
        adapter = TushareAdapter(
            token=settings.TUSHARE_TOKEN,
            api_url=settings.TUSHARE_API_URL
        )
        print(f"✅ 适配器初始化成功")
        return adapter
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_get_daily_data(adapter):
    """测试获取日线数据"""
    print("\n" + "=" * 60)
    print("测试1：获取日线数据（平安银行 000001.SZ）")
    print("=" * 60)

    try:
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')

        df = adapter.get_daily_data(
            symbol='000001.SZ',
            start_date=start_date,
            end_date=end_date
        )

        print(f"✅ 成功获取 {len(df)} 条日线数据")
        print("\n前 5 天数据：")
        print(df.head())

        if len(df) > 0:
            print(f"\n最新数据：")
            print(f"日期: {df.iloc[-1]['date']}")
            print(f"收盘价: {df.iloc[-1]['close']:.2f}")
            print(f"成交量: {df.iloc[-1]['volume']:.0f}")

        return True
    except Exception as e:
        print(f"❌ 获取日线数据失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_get_trade_calendar(adapter):
    """测试获取交易日历"""
    print("\n" + "=" * 60)
    print("测试2：获取交易日历（2026年1月）")
    print("=" * 60)

    try:
        df = adapter.get_trade_calendar(
            exchange='SSE',
            start_date='20260101',
            end_date='20260131'
        )

        print(f"✅ 成功获取 {len(df)} 条交易日历数据")
        print("\n前 10 天：")
        print(df.head(10))

        # 统计交易日
        trading_days = df[df['is_open'] == 1]
        print(f"\n交易日统计：共 {len(trading_days)} 个交易日")

        return True
    except Exception as e:
        print(f"❌ 获取交易日历失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_tests():
    """运行所有测试"""
    print("\n" + "🚀 开始测试 Tushare 适配器" + "\n")

    # 测试初始化
    adapter = test_tushare_adapter()
    if not adapter:
        print("\n❌ 适配器初始化失败，无法继续测试")
        return 1

    # 测试功能
    tests = [
        ("日线数据", lambda: test_get_daily_data(adapter)),
        ("交易日历", lambda: test_get_trade_calendar(adapter))
    ]

    results = {}
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = "✅ 通过" if result else "❌ 失败"
        except Exception as e:
            results[test_name] = f"❌ 错误: {str(e)}"
            print(f"\n❌ {test_name} 测试出错: {e}")

    # 打印总结
    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)

    for test_name, result in results.items():
        print(f"{test_name}: {result}")

    passed = sum(1 for r in results.values() if "✅" in r)
    total = len(results)

    print("\n" + "=" * 60)
    print(f"通过率: {passed}/{total} ({passed/total*100:.1f}%)")
    print("=" * 60)

    if passed == total:
        print("\n🎉 所有 Tushare 测试通过！数据源配置正确。")
        return 0
    else:
        print("\n⚠️ 部分测试失败，请检查。")
        return 1


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
