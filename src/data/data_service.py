"""
数据服务主类
"""
import pandas as pd
from typing import Optional, Dict
from pathlib import Path
import json
from .adapters.tushare_adapter import TushareAdapter
from ..utils.logger import logger
from ..utils.config import settings


class DataService:
    """数据服务主类"""

    def __init__(self, adapter: Optional[TushareAdapter] = None):
        """
        初始化数据服务

        Args:
            adapter: 数据源适配器，如果为 None 则使用 Tushare
        """
        if adapter is None:
            if not settings.TUSHARE_TOKEN:
                raise ValueError("TUSHARE_TOKEN 未配置")
            self.adapter = TushareAdapter(settings.TUSHARE_TOKEN)
        else:
            self.adapter = adapter

        # 缓存目录
        self.cache_dir = Path(settings.DATA_CACHE_DIR)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        logger.info("数据服务初始化成功")

    def get_daily_data(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        use_cache: bool = True
    ) -> pd.DataFrame:
        """
        获取日线数据

        Args:
            symbol: 股票代码
            start_date: 开始日期
            end_date: 结束日期
            use_cache: 是否使用缓存

        Returns:
            DataFrame
        """
        cache_key = f"daily_{symbol}_{start_date}_{end_date}"
        cache_file = self.cache_dir / f"{cache_key}.parquet"

        # 尝试从缓存读取
        if use_cache and cache_file.exists():
            logger.info(f"从缓存读取数据: {cache_file}")
            df = pd.read_parquet(cache_file)
            return df

        # 从数据源获取
        df = self.adapter.get_daily_data(symbol, start_date, end_date)

        # 保存到缓存
        if use_cache and not df.empty:
            df.to_parquet(cache_file, index=False)
            logger.info(f"数据已缓存: {cache_file}")

        return df

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
        cache_key = f"calendar_{exchange}_{start_date}_{end_date}"
        cache_file = self.cache_dir / f"{cache_key}.parquet"

        # 尝试从缓存读取
        if cache_file.exists():
            logger.info(f"从缓存读取交易日历: {cache_file}")
            return pd.read_parquet(cache_file)

        # 从数据源获取
        df = self.adapter.get_trade_calendar(exchange, start_date, end_date)

        # 保存到缓存
        if not df.empty:
            df.to_parquet(cache_file, index=False)
            logger.info(f"交易日历已缓存: {cache_file}")

        return df

    def is_trading_day(
        self,
        date: str,
        exchange: str = 'SSE'
    ) -> bool:
        """
        判断是否为交易日

        Args:
            date: 日期，格式 'YYYY-MM-DD'
            exchange: 交易所代码

        Returns:
            是否为交易日
        """
        df = self.get_trade_calendar(exchange, date[:4], date[:4])
        date_fmt = date.replace('-', '')
        row = df[df['date'] == date_fmt]
        return not row.empty and row.iloc[0]['is_open'] == 1

    def update_data(
        self,
        symbols: list,
        start_date: str,
        end_date: str
    ) -> Dict[str, bool]:
        """
        批量更新数据

        Args:
            symbols: 股票代码列表
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            更新结果
        """
        results = {}

        for symbol in symbols:
            try:
                logger.info(f"更新数据: {symbol}")
                df = self.get_daily_data(symbol, start_date, end_date, use_cache=False)
                results[symbol] = not df.empty
            except Exception as e:
                logger.error(f"更新数据失败 {symbol}: {e}")
                results[symbol] = False

        success_count = sum(1 for v in results.values() if v)
        logger.info(f"数据更新完成: {success_count}/{len(symbols)} 成功")

        return results
