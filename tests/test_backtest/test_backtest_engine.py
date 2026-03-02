"""
测试回测引擎
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.backtest.backtest_engine import BacktestEngine, BacktestConfig, generate_double_ma_signal


def create_test_data():
    """创建测试数据"""
    # 生成 60 天的测试数据
    dates = [datetime(2023, 1, 1) + timedelta(days=i) for i in range(60)]

    # 生成价格数据（简单的上升趋势）
    np.random.seed(42)
    base_price = 10.0
    prices = [base_price]
    for i in range(1, 60):
        change = np.random.randn() * 0.02 + 0.001  # 随机波动 + 小幅上涨
        prices.append(prices[-1] * (1 + change))

    data = pd.DataFrame({
        'date': dates,
        'open': prices,
        'high': [p * 1.02 for p in prices],
        'low': [p * 0.98 for p in prices],
        'close': prices,
        'volume': [1000000] * 60
    })

    return data


def test_backtest_config():
    """测试回测配置"""
    print("\n" + "=" * 50)
    print("测试回测配置")
    print("=" * 50)

    config = BacktestConfig(
        symbol='000001.SZ',
        start_date='2023-01-01',
        end_date='2023-03-01',
        initial_cash=100000.0
    )

    print(f"✅ 股票代码: {config.symbol}")
    print(f"✅ 开始日期: {config.start_date}")
    print(f"✅ 结束日期: {config.end_date}")
    print(f"✅ 初始资金: {config.initial_cash}")
    print(f"✅ 佣金率: {config.commission}")
    print(f"✅ 印花税: {config.stamp_tax}")

    return True


def test_backtest_engine():
    """测试回测引擎"""
    print("\n" + "=" * 50)
    print("测试回测引擎")
    print("=" * 50)

    # 创建测试数据
    data = create_test_data()
    print(f"✅ 创建测试数据: {len(data)} 行")

    # 生成信号
    signals = generate_double_ma_signal(data, fast_period=5, slow_period=20)
    print(f"✅ 生成双均线信号: {len(signals)} 行")

    # 创建回测配置
    config = BacktestConfig(
        symbol='TEST.SZ',
        start_date=data['date'].min().strftime('%Y-%m-%d'),
        end_date=data['date'].max().strftime('%Y-%m-%d'),
        initial_cash=100000.0
    )

    # 运行回测
    engine = BacktestEngine(config)
    result = engine.run(data, signals)

    print(f"✅ 总收益率: {result.total_return:.2%}")
    print(f"✅ 年化收益率: {result.annual_return:.2%}")
    print(f"✅ 最大回撤: {result.max_drawdown:.2%}")
    print(f"✅ 夏普比率: {result.sharpe_ratio:.2f}")
    print(f"✅ 胜率: {result.win_rate:.2%}")
    print(f"✅ 盈亏比: {result.profit_loss_ratio:.2f}")
    print(f"✅ 交易次数: {result.total_trades}")

    # 验证结果
    assert isinstance(result.total_return, float)
    assert isinstance(result.annual_return, float)
    assert isinstance(result.max_drawdown, float)
    assert isinstance(result.sharpe_ratio, float)
    assert isinstance(result.daily_values, pd.DataFrame)
    assert isinstance(result.trades, list)

    return True


def test_double_ma_signal():
    """测试双均线信号生成"""
    print("\n" + "=" * 50)
    print("测试双均线信号生成")
    print("=" * 50)

    # 创建测试数据
    data = create_test_data()

    # 生成信号
    signals = generate_double_ma_signal(data, fast_period=5, slow_period=20)

    print(f"✅ 信号数量: {len(signals)}")
    print(f"✅ 买入信号: {(signals['signal'] == 1).sum()}")
    print(f"✅ 卖出信号: {(signals['signal'] == -1).sum()}")
    print(f"✅ 持有信号: {(signals['signal'] == 0).sum()}")

    # 验证信号
    assert 'date' in signals.columns
    assert 'signal' in signals.columns
    assert signals['signal'].isin([1, -1, 0]).all()

    return True


def run_all_tests():
    """运行所有测试"""
    print("\n" + "🚀 开始运行回测引擎测试" + "\n")

    tests = [
        ("回测配置", test_backtest_config),
        ("双均线信号", test_double_ma_signal),
        ("回测引擎", test_backtest_engine)
    ]

    results = {}

    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = "✅ 通过" if result else "❌ 失败"
        except Exception as e:
            results[test_name] = f"❌ 错误: {str(e)}"
            print(f"\n❌ {test_name} 测试出错: {e}")
            import traceback
            traceback.print_exc()

    # 打印总结
    print("\n" + "=" * 50)
    print("📊 测试总结")
    print("=" * 50)

    for test_name, result in results.items():
        print(f"{test_name}: {result}")

    passed = sum(1 for r in results.values() if "✅" in r)
    total = len(results)

    print("\n" + "=" * 50)
    print(f"通过率: {passed}/{total} ({passed/total*100:.1f}%)")
    print("=" * 50)

    if passed == total:
        print("\n🎉 所有回测引擎测试通过！")
        return 0
    else:
        print("\n⚠️ 部分测试失败，请检查。")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
