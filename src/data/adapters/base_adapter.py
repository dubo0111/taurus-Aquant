"""
数据源适配器基类
"""
from abc import ABC, abstractmethod
from typing import Optional
import pandas as pd


class DataSourceAdapter(ABC):
    """数据源适配器抽象基类"""

    @abstractmethod
    def get_daily_data(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        **kwargs
    ) -> pd.DataFrame:
        """
        获取日线数据

        Args:
            symbol: 股票代码，如 '000001.SZ'
            start_date: 开始日期，格式 'YYYY-MM-DD'
            end_date: 结束日期，格式 'YYYY-MM-DD'

        Returns:
            DataFrame，包含列：date, open, high, low, close, volume
        """
        pass

    @abstractmethod
    def get_minute_data(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        freq: str = '1min',
        **kwargs
    ) -> pd.DataFrame:
        """
        获取分钟线数据

        Args:
            symbol: 股票代码
            start_date: 开始日期
            end_date: 结束日期
            freq: 频率，如 '1min', '5min', '15min', '30min', '60min'

        Returns:
            DataFrame
        """
        pass

    @abstractmethod
    def get_trade_calendar(
        self,
        exchange: str = 'SSE',
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        获取交易日历

        Args:
            exchange: 交易所代码，'SSE' (上交所) 或 'SZSE' (深交所)
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            DataFrame，包含列：exchange, cal_date, is_open, pretrade_date
        """
        pass

    @abstractmethod
    def get_stock_list(self, exchange: str = 'SSE') -> pd.DataFrame:
        """
        获取股票列表

        Args:
            exchange: 交易所代码

        Returns:
            DataFrame，包含列：ts_code, symbol, name, area, industry, market, list_date
        """
        pass

    def validate_data(self, df: pd.DataFrame) -> bool:
        """
        验证数据格式是否正确

        Args:
            df: 数据 DataFrame

        Returns:
            是否通过验证
        """
        required_columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        return all(col in df.columns for col in required_columns)

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        清洗数据

        Args:
            df: 原始数据

        Returns:
            清洗后的数据
        """
        if df.empty:
            return df

        # 删除重复行
        df = df.drop_duplicates()

        # 删除全为 NaN 的行
        df = df.dropna(how='all')

        # 按日期排序
        if 'date' in df.columns:
            df = df.sort_values('date').reset_index(drop=True)

        return df
