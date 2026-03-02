"""
测试 AkShare 数据获取（免费，无需 Token）
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data.data_service import DataService
from src.utils.logger import logger


def test_akshare_connection():
    """测试 AkShare 数据源"""
    print("=" * 60)
    print("测试 AkShare 数据源（免费，无需 Token）")
    print("=" * 60)

    try:
        data_service = DataService()
        print(f"✅ 数据服务初始化成功")
        print(f"✅ 使用适配器: {data_service.adapter.__class__.__name__}")
        return data_service
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return None


def test_get_stock_list(data_service):
    """测试获取股票列表"""
    print("\n" + "=" * 60)
    print("测试获取股票列表（上交所）")
    print("=" * 60)

    try:
        df = data_service.get_stock_list(exchange='SSE')
        print(f"✅ 获取股票列表成功，共 {len(df)} 只股票")
        print("\n前 5 只股票：")
        print(df.head())

        return True
    except Exception as e:
        print(f"❌ 获取股票列表失败: {e}")
        return False


def test_get_trade_calendar(data_service):
    """测试获取交易日历"""
    print("\n" + "=" * 60)
    print("测试获取交易日历")
    print("=" * 60)

    try:
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

        df = data_service.get_trade_calendar(
            exchange='SSE',
            start_date=start_date,
            end_date=end_date
        )

        print(f"✅ 获取交易日历成功，共 {len(df)} 天")
        print("\n交易日历示例：")
        print(df.head(10))

        return True
    except Exception as e:
        print(f"❌ 获取交易日历失败: {e}")
        return False


def test_get_daily_data(data_service):
    """测试获取日线数据"""
    print("\n" + "=" * 60)
    print("测试获取日线数据（平安银行 000001）")
    print("=" * 60)

    try:
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

        df = data_service.get_daily_data(
            symbol='000001',
            start_date=start_date,
            end_date=end_date
        )

        print(f"✅ 获取日线数据成功，共 {len(df)} 条记录")
        print("\n前 5 天数据：")
        print(df.head())

        if len(df) > 0:
            print(f"\n最新收盘价: {df.iloc[-1]['close']:.2f}")
            print(f"最高价: {df['high'].max():.2f}")
            print(f"最低价: {df['low'].min():.2f}")
            print(f"平均成交量: {df['volume'].mean():.0f}")

        return True
    except Exception as e:
        print(f"❌ 获取日线数据失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """运行所有测试"""
    print("\n" + "🚀 开始测试 AkShare 数据源" + "\n")

    # 测试连接
    data_service = test_akshare_connection()
    if not data_service:
        print("\n❌ 数据服务初始化失败，无法继续测试")
        return 1

    # 测试各项功能
    tests = [
        ("股票列表", lambda: test_get_stock_list(data_service)),
        ("交易日历", lambda: test_get_trade_calendar(data_service)),
        ("日线数据", lambda: test_get_daily_data(data_service))
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
        print("\n🎉 所有 AkShare 测试通过！数据源配置正确。")
        return 0
    else:
        print("\n⚠️ 部分测试失败，请检查。")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
