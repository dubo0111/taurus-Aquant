"""
基础功能测试脚本（无需外部依赖）
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_config():
    """测试配置模块"""
    print("=" * 50)
    print("测试配置模块")
    print("=" * 50)

    from src.utils.config import Settings

    # 创建配置实例
    settings = Settings()

    print(f"✅ APP_NAME: {settings.APP_NAME}")
    print(f"✅ APP_VERSION: {settings.APP_VERSION}")
    print(f"✅ LLM_PROVIDER: {settings.LLM_PROVIDER}")
    print(f"✅ 数据库 URL: {settings.database_url}")
    print(f"✅ Redis URL: {settings.redis_url}")

    return True


def test_logger():
    """测试日志模块"""
    print("\n" + "=" * 50)
    print("测试日志模块")
    print("=" * 50)

    from src.utils.logger import logger

    logger.info("这是一条 INFO 日志")
    logger.warning("这是一条 WARNING 日志")
    logger.error("这是一条 ERROR 日志")

    print("✅ 日志模块正常工作")
    return True


def test_data_adapter():
    """测试数据适配器基类"""
    print("\n" + "=" * 50)
    print("测试数据适配器基类")
    print("=" * 50)

    from src.data.adapters.base_adapter import DataSourceAdapter
    import pandas as pd

    # 创建测试数据
    test_df = pd.DataFrame({
        'date': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'open': [10.0, 10.5, 10.2],
        'high': [10.5, 11.0, 10.8],
        'low': [9.8, 10.2, 10.0],
        'close': [10.2, 10.8, 10.5],
        'volume': [100000, 120000, 110000]
    })

    # 测试验证方法
    class TestAdapter(DataSourceAdapter):
        def get_daily_data(self, symbol, start_date, end_date, **kwargs):
            pass

        def get_minute_data(self, symbol, start_date, end_date, freq='1min', **kwargs):
            pass

        def get_trade_calendar(self, exchange='SSE', start_date=None, end_date=None):
            pass

        def get_stock_list(self, exchange='SSE'):
            pass

    adapter = TestAdapter()

    # 验证数据
    is_valid = adapter.validate_data(test_df)
    print(f"✅ 数据验证: {is_valid}")

    # 清洗数据
    cleaned_df = adapter.clean_data(test_df)
    print(f"✅ 数据清洗: {len(cleaned_df)} 行")

    return True


def test_directory_structure():
    """测试目录结构"""
    print("\n" + "=" * 50)
    print("测试目录结构")
    print("=" * 50)

    required_dirs = [
        "src/api",
        "src/backtest",
        "src/data",
        "src/agent",
        "src/trading",
        "src/risk",
        "src/ui",
        "src/utils",
        "tests",
        "docs",
        "configs",
        "scripts",
        "logs",
        "data"
    ]

    project_root = Path(__file__).parent.parent

    for dir_path in required_dirs:
        full_path = project_root / dir_path
        if full_path.exists():
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path} 不存在")
            return False

    return True


def test_file_structure():
    """测试文件结构"""
    print("\n" + "=" * 50)
    print("测试文件结构")
    print("=" * 50)

    required_files = [
        "README.md",
        "requirements.txt",
        ".env.example",
        ".gitignore",
        "docs/PRD.md",
        "docs/ARCHITECTURE.md",
        "docs/QUICKSTART.md",
        "src/utils/config.py",
        "src/utils/logger.py",
        "src/data/adapters/base_adapter.py",
        "src/data/adapters/tushare_adapter.py",
        "src/data/data_service.py"
    ]

    project_root = Path(__file__).parent.parent

    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} 不存在")
            return False

    return True


def run_all_tests():
    """运行所有测试"""
    print("\n" + "🚀 开始运行基础功能测试" + "\n")

    tests = [
        ("目录结构", test_directory_structure),
        ("文件结构", test_file_structure),
        ("配置模块", test_config),
        ("日志模块", test_logger),
        ("数据适配器", test_data_adapter)
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
        print("\n🎉 所有测试通过！可以继续开发。")
        return 0
    else:
        print("\n⚠️ 部分测试失败，请检查。")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
