"""
测试 Tushare 数据获取
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data.adapters.tushare_adapter import TushareAdapter
from src.utils.config import settings
from src.utils.logger import logger


def test_tushare_connection():
    """测试 Tushare API 连接"""
    print("=" * 60)
    print("测试 Tushare API 连接")
    print("=" * 60)

    try:
        adapter = TushareAdapter(settings.TUSHARE_TOKEN)
        print(f"✅ Tushare 适配器初始化成功")
        print(f"✅ Token: {settings.TUSHARE_TOKEN[:10]}...")
        return adapter
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return None


def test_get_stock_list(adapter):
    """测试获取股票列表"""
    print("\n" + "=" * 60)
    print("测试获取股票列表")
    print("=" * 60)

    try:
        df = adapter.get_stock_list(exchange='SSE')
        print(f"✅ 获取到 {len(df)} 只股票")
        print(f"✅ 列名: {df.columns.tolist()}")
        print(f"\n前 5 只股票:")
        print(df.head())
        return True
    except Exception as e:
        print(f"❌ 获取股票列表失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_get_trade_calendar(adapter):
    """测试获取交易日历"""
    print("\n" + "=" * 60)
    print("测试获取交易日历")
    print("=" * 60)

    try:
        # 获取最近 30 天的交易日历
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        df = adapter.get_trade_calendar(
            exchange='SSE',
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d')
        )

        print(f"✅ 获取到 {len(df)} 条交易日历")
        print(f"✅ 列名: {df.columns.tolist()}")

        # 显示最近的交易日
        trading_days = df[df['is_open'] == 1]
        print(f"✅ 交易日数量: {len(trading_days)}")

        if not trading_days.empty:
            print(f"\n最近 5 个交易日:")
            print(trading_days.tail())

        return True
    except Exception as e:
        print(f"❌ 获取交易日历失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_get_daily_data(adapter):
    """测试获取日线数据"""
    print("\n" + "=" * 60)
    print("测试获取日线数据（平安银行 000001.SZ）")
    print("=" * 60)

    try:
        # 获取最近 30 天的数据
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        df = adapter.get_daily_data(
            symbol='000001.SZ',
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d')
        )

        if df.empty:
            print("⚠️ 未获取到数据（可能是非交易日或 Token 权限不足）")
            return False

        print(f"✅ 获取到 {len(df)} 条日线数据")
        print(f"✅ 列名: {df.columns.tolist()}")
        print(f"✅ 数据验证: {adapter.validate_data(df)}")

        print(f"\n数据预览:")
        print(df.tail())

        print(f"\n数据统计:")
        print(df.describe())

        return True
    except Exception as e:
        print(f"❌ 获取日线数据失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """运行所有测试"""
    print("\n" + "🚀 开始测试 Tushare API" + "\n")

    # 测试连接
    adapter = test_tushare_connection()
    if not adapter:
        print("\n❌ 无法连接到 Tushare API，请检查 Token")
        return 1

    # 运行测试
    tests = [
        ("股票列表", test_get_stock_list),
        ("交易日历", test_get_trade_calendar),
        ("日线数据", test_get_daily_data)
    ]

    results = {}

    for test_name, test_func in tests:
        try:
            result = test_func(adapter)
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
        print("\n🎉 所有 Tushare API 测试通过！")
        return 0
    else:
        print("\n⚠️ 部分测试失败，请检查。")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
