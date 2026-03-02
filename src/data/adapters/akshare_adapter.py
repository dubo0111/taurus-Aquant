"""
AkShare 数据源适配器（免费，无需 Token）
"""
import akshare as ak
import pandas as pd
from typing import Optional
from .base_adapter import DataSourceAdapter
from ...utils.logger import logger


class AkShareAdapter(DataSourceAdapter):
    """AkShare 数据源适配器"""

    def __init__(self):
        """初始化 AkShare 适配器"""
        logger.info("AkShare 适配器初始化成功（免费，无需 Token）")

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
            symbol: 股票代码，如 '000001'（不带后缀）
            start_date: 开始日期，格式 'YYYY-MM-DD'
            end_date: 结束日期，格式 'YYYY-MM-DD'

        Returns:
            DataFrame，标准列：date, open, high, low, close, volume
        """
        try:
            logger.info(f"获取日线数据: {symbol}, {start_date} - {end_date}")

            # AkShare 使用不带后缀的股票代码
            code = symbol.split('.')[0]

            # 获取数据
            df = ak.stock_zh_a_hist(
                symbol=code,
                period="daily",
                start_date=start_date.replace('-', ''),
                end_date=end_date.replace('-', ''),
                adjust=""
            )

            if df.empty:
                logger.warning(f"未获取到数据: {symbol}")
                return pd.DataFrame()

            # 转换为标准格式
            df = df.rename(columns={
                '日期': 'date',
                '开盘': 'open',
                '最高': 'high',
                '最低': 'low',
                '收盘': 'close',
                '成交量': 'volume'
            })

            # 转换日期格式
            df['date'] = pd.to_datetime(df['date'])

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
        获取分钟线数据（AkShare 暂不支持）

        Args:
            symbol: 股票代码
            start_date: 开始日期
            end_date: 结束日期
            freq: 频率

        Returns:
            DataFrame
        """
        logger.warning("AkShare 暂不支持分钟线数据，请使用日线数据")
        return pd.DataFrame()

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

            # 获取交易日历
            df = ak.tool_trade_date_hist_sina()

            if df.empty:
                logger.warning("未获取到交易日历数据")
                return pd.DataFrame()

            # 转换为标准格式
            df = df.rename(columns={'trade_date': 'date'})
            df['date'] = pd.to_datetime(df['date'])
            df['is_open'] = 1
            df['exchange'] = exchange

            # 过滤日期范围
            if start_date:
                start_dt = pd.to_datetime(start_date)
                df = df[df['date'] >= start_dt]
            if end_date:
                end_dt = pd.to_datetime(end_date)
                df = df[df['date'] <= end_dt]

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

            # 获取 A 股列表
            df = ak.stock_info_a_code_name()

            if df.empty:
                logger.warning("未获取到股票列表")
                return pd.DataFrame()

            # 转换为标准格式
            df = df.rename(columns={
                'code': 'symbol',
                'name': 'name'
            })

            # 添加交易所后缀
            if exchange == 'SSE':
                df = df[df['symbol'].str.startswith(('6', '5'))]
                df['ts_code'] = df['symbol'] + '.SH'
            else:  # SZSE
                df = df[df['symbol'].str.startswith(('0', '3'))]
                df['ts_code'] = df['symbol'] + '.SZ'

            logger.info(f"成功获取 {len(df)} 只股票")

            return df

        except Exception as e:
            logger.error(f"获取股票列表失败: {e}")
            raise
