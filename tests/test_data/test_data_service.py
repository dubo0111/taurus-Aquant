"""
测试数据服务
"""
import pytest
import pandas as pd
from unittest.mock import Mock, patch
from src.data.data_service import DataService
from src.data.adapters.tushare_adapter import TushareAdapter


class TestTushareAdapter:
    """测试 Tushare 适配器"""

    @pytest.fixture
    def adapter(self):
        """创建适配器实例"""
        with patch('tushare.pro_api') as mock_pro_api:
            mock_pro = Mock()
            mock_pro_api.return_value = mock_pro
            adapter = TushareAdapter(token="test_token")
            return adapter

    def test_get_daily_data(self, adapter):
        """测试获取日线数据"""
        # Mock 数据
        mock_df = pd.DataFrame({
            'trade_date': ['20230101', '20230102'],
            'open': [10.0, 10.5],
            'high': [10.5, 11.0],
            'low': [9.8, 10.2],
            'close': [10.2, 10.8],
            'vol': [100000, 120000]
        })

        adapter.pro.daily.return_value = mock_df

        # 调用方法
        result = adapter.get_daily_data('000001.SZ', '2023-01-01', '2023-01-02')

        # 验证
        assert not result.empty
        assert 'date' in result.columns
        assert 'close' in result.columns
        assert len(result) == 2

    def test_get_trade_calendar(self, adapter):
        """测试获取交易日历"""
        # Mock 数据
        mock_df = pd.DataFrame({
            'exchange': ['SSE', 'SSE'],
            'cal_date': ['20230101', '20230102'],
            'is_open': [1, 1],
            'pretrade_date': ['20221230', '20230101']
        })

        adapter.pro.trade_cal.return_value = mock_df

        # 调用方法
        result = adapter.get_trade_calendar('SSE', '2023-01-01', '2023-01-02')

        # 验证
        assert not result.empty
        assert 'date' in result.columns
        assert len(result) == 2


class TestDataService:
    """测试数据服务"""

    @pytest.fixture
    def data_service(self, tmp_path):
        """创建数据服务实例"""
        with patch('src.utils.config.settings') as mock_settings:
            mock_settings.TUSHARE_TOKEN = "test_token"
            mock_settings.DATA_CACHE_DIR = str(tmp_path / "cache")

            with patch('tushare.pro_api') as mock_pro_api:
                mock_pro = Mock()
                mock_pro_api.return_value = mock_pro

                service = DataService()
                return service

    def test_get_daily_data_with_cache(self, data_service, tmp_path):
        """测试获取数据（带缓存）"""
        # Mock 数据
        mock_df = pd.DataFrame({
            'trade_date': ['20230101'],
            'open': [10.0],
            'high': [10.5],
            'low': [9.8],
            'close': [10.2],
            'vol': [100000]
        })

        data_service.adapter.pro.daily.return_value = mock_df

        # 第一次调用（从数据源获取）
        result1 = data_service.get_daily_data('000001.SZ', '2023-01-01', '2023-01-01')
        assert not result1.empty

        # 第二次调用（从缓存读取）
        result2 = data_service.get_daily_data('000001.SZ', '2023-01-01', '2023-01-01')
        assert not result2.empty

    def test_is_trade_day(self, data_service):
        """测试判断交易日"""
        # Mock 交易日历
        mock_calendar = pd.DataFrame({
            'date': pd.to_datetime(['2023-01-03', '2023-01-04']),
            'is_open': [1, 1]
        })

        with patch.object(data_service, 'get_trade_calendar', return_value=mock_calendar):
            # 测试交易日
            assert data_service.is_trade_day('2023-01-03') is True

            # 测试非交易日
            assert data_service.is_trade_day('2023-01-01') is False


def test_adapter_validate_data():
    """测试数据验证"""
    from src.data.adapters.base_adapter import DataSourceAdapter

    # 创建一个简单的实现类
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

    # 测试有效数据
    valid_df = pd.DataFrame({
        'date': ['2023-01-01'],
        'open': [10.0],
        'high': [10.5],
        'low': [9.8],
        'close': [10.2],
        'volume': [100000]
    })
    assert adapter.validate_data(valid_df) is True

    # 测试无效数据
    invalid_df = pd.DataFrame({
        'date': ['2023-01-01'],
        'close': [10.2]
    })
    assert adapter.validate_data(invalid_df) is False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
