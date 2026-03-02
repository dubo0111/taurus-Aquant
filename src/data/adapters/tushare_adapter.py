"""
Tushare 数据源适配器
"""
import tushare as ts
import tushare.pro.client as client
import pandas as pd
from typing import Optional
from .base_adapter import DataSourceAdapter
from ...utils.logger import logger
from ...utils.config import settings


class TushareAdapter(DataSourceAdapter):
    """Tushare 数据源适配器"""

    def __init__(self, token: str, api_url: Optional[str] = None):
        """
        初始化 Tushare 适配器

        Args:
            token: Tushare API Token
            api_url: Tushare API URL（可选，用于第三方镜像）
        """
        self.token = token
        self.api_url = api_url or getattr(settings, 'TUSHARE_API_URL', None)

        # 设置自定义 API URL（用于第三方镜像）
        if self.api_url:
            # 注意：必须在 ts.pro_api() 之前设置
            client.DataApi._DataApi__http_url = self.api_url
            logger.info(f"使用自定义 Tushare API URL: {self.api_url}")

        # 初始化 pro_api
        self.pro = ts.pro_api(token)
        logger.info(f"Tushare 适配器初始化成功")

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
            start_date: 开始日期，格式 'YYYY-MM-DD' 或 'YYYYMMDD'
            end_date: 结束日期，格式 'YYYY-MM-DD' 或 'YYYYMMDD'

        Returns:
            DataFrame，标准列：date, open, high, low, close, volume
        """
        try:
            # 格式化日期
            start_date_fmt = start_date.replace('-', '')
            end_date_fmt = end_date.replace('-', '')

            logger.info(f"获取日线数据: {symbol}, {start_date} - {end_date}")

            # 调用 Tushare API
            df = self.pro.daily(
                ts_code=symbol,
                start_date=start_date_fmt,
                end_date=end_date_fmt
            )

            if df.empty:
                logger.warning(f"未获取到数据: {symbol}")
                return pd.DataFrame()

            # 转换为标准格式
            df = df.rename(columns={
                'trade_date': 'date',
                'vol': 'volume'
            })

            # 转换日期格式
            df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')

            # 选择需要的列
            df = df[['date', 'open', 'high', 'low', 'close', 'volume']]

            # 清洗数据
            df = self.clean_data(df)

            logger.info(f"成功获取 {len(df)} 条日线数据")

            return df

        except Exception as e:
            logger.error(f"获取日线数据失败: {e}")
            raise

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
            freq: 频率

        Returns:
            DataFrame
        """
        try:
            logger.info(f"获取分钟线数据: {symbol}, {freq}, {start_date} - {end_date}")

            # 注意：分钟线数据需要更高权限
            start_date_fmt = start_date.replace('-', '')
            end_date_fmt = end_date.replace('-', '')

            df = self.pro.stk_mins(
                ts_code=symbol,
                start_date=start_date_fmt,
                end_date=end_date_fmt,
                freq=freq
            )

            if df.empty:
                logger.warning(f"未获取到分钟数据: {symbol}")
                return pd.DataFrame()

            # 转换为标准格式
            df = df.rename(columns={
                'trade_time': 'date',
                'vol': 'volume'
            })

            df['date'] = pd.to_datetime(df['date'])
            df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
            df = self.clean_data(df)

            logger.info(f"成功获取 {len(df)} 条分钟数据")

            return df

        except Exception as e:
            logger.error(f"获取分钟数据失败: {e}")
            raise

    def get_trade_calendar(
        self,
        exchange: str = 'SSE',
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        获取交易日历

        Args:
            exchange: 交易所代码
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            DataFrame
        """
        try:
            logger.info(f"获取交易日历: {exchange}, {start_date} - {end_date}")

            start_date_fmt = start_date.replace('-', '') if start_date else None
            end_date_fmt = end_date.replace('-', '') if end_date else None

            df = self.pro.trade_cal(
                exchange=exchange,
                start_date=start_date_fmt,
                end_date=end_date_fmt
            )

            df = df.rename(columns={'cal_date': 'date'})
            df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')

            logger.info(f"成功获取 {len(df)} 条交易日历数据")

            return df

        except Exception as e:
            logger.error(f"获取交易日历失败: {e}")
            raise

    def get_stock_list(self, exchange: str = 'SSE') -> pd.DataFrame:
        """
        获取股票列表

        Args:
            exchange: 交易所代码

        Returns:
            DataFrame
        """
        try:
            logger.info(f"获取股票列表: {exchange}")

            df = self.pro.stock_basic(exchange=exchange, list_status='L')

            logger.info(f"成功获取 {len(df)} 只股票")

            return df

        except Exception as e:
            logger.error(f"获取股票列表失败: {e}")
            raise
