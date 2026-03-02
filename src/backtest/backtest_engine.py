"""
回测引擎模块（简化版）
"""
import pandas as pd
import numpy as np
from typing import Optional, Dict, List
from dataclasses import dataclass
from datetime import datetime
from ..utils.logger import logger


@dataclass
class BacktestConfig:
    """回测配置"""
    symbol: str
    start_date: str
    end_date: str
    initial_cash: float = 100000.0
    commission: float = 0.0003  # 佣金率万三
    stamp_tax: float = 0.001    # 印花税千一
    slippage: float = 0.0       # 滑点


@dataclass
class BacktestResult:
    """回测结果"""
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    profit_loss_ratio: float
    total_trades: int
    daily_values: pd.DataFrame
    trades: List[Dict]


class BacktestEngine:
    """回测引擎（简化版）"""

    def __init__(self, config: BacktestConfig):
        """初始化回测引擎"""
        self.config = config
        self.cash = config.initial_cash
        self.positions = 0
        self.trades = []
        self.daily_values = []

        logger.info(f"回测引擎初始化: {config.symbol}, {config.start_date} - {config.end_date}")

    def run(self, data: pd.DataFrame, signals: pd.DataFrame) -> BacktestResult:
        """
        执行回测

        Args:
            data: 价格数据，包含 date, open, high, low, close, volume
            signals: 信号数据，包含 date, signal (1=买入, -1=卖出, 0=持有)

        Returns:
            回测结果
        """
        logger.info("开始执行回测...")

        # 合并数据和信号
        df = pd.merge(data, signals[['date', 'signal']], on='date', how='left')
        df['signal'] = df['signal'].fillna(0)

        # 初始化持仓
        self.cash = self.config.initial_cash
        self.positions = 0
        self.trades = []
        self.daily_values = []

        # 逐日回测
        for idx, row in df.iterrows():
            date = row['date']
            close = row['close']
            signal = row['signal']

            # 执行交易
            if signal == 1 and self.positions == 0:  # 买入
                shares = int(self.cash / close)
                if shares > 0:
                    cost = shares * close * (1 + self.config.commission)
                    if cost <= self.cash:
                        self.cash -= cost
                        self.positions = shares
                        self.trades.append({
                            'date': date,
                            'action': 'buy',
                            'price': close,
                            'shares': shares,
                            'cost': cost
                        })
                        logger.debug(f"{date}: 买入 {shares} 股，价格 {close:.2f}，成本 {cost:.2f}")

            elif signal == -1 and self.positions > 0:  # 卖出
                revenue = self.positions * close * (1 - self.config.commission - self.config.stamp_tax)
                self.cash += revenue
                profit = revenue - self.trades[-1]['cost']
                self.trades[-1]['sell_date'] = date
                self.trades[-1]['sell_price'] = close
                self.trades[-1]['revenue'] = revenue
                self.trades[-1]['profit'] = profit
                logger.debug(f"{date}: 卖出 {self.positions} 股，价格 {close:.2f}，收入 {revenue:.2f}，盈利 {profit:.2f}")
                self.positions = 0

            # 记录每日价值
            total_value = self.cash + self.positions * close
            self.daily_values.append({
                'date': date,
                'cash': self.cash,
                'positions': self.positions,
                'position_value': self.positions * close,
                'total_value': total_value
            })

        # 转换为 DataFrame
        daily_values_df = pd.DataFrame(self.daily_values)

        # 计算绩效指标
        result = self._calculate_metrics(daily_values_df)

        logger.info(f"回测完成: 年化收益 {result.annual_return:.2%}, 最大回撤 {result.max_drawdown:.2%}")

        return result

    def _calculate_metrics(self, daily_values: pd.DataFrame) -> BacktestResult:
        """计算绩效指标"""
        # 总收益率
        total_return = (daily_values['total_value'].iloc[-1] / self.config.initial_cash - 1)

        # 年化收益率
        days = (daily_values['date'].iloc[-1] - daily_values['date'].iloc[0]).days
        annual_return = (1 + total_return) ** (365 / days) - 1 if days > 0 else 0

        # 日收益率
        daily_values['daily_return'] = daily_values['total_value'].pct_change()

        # 最大回撤
        cumulative_max = daily_values['total_value'].cummax()
        drawdown = (daily_values['total_value'] - cumulative_max) / cumulative_max
        max_drawdown = drawdown.min()

        # 夏普比率（假设无风险利率为 3%）
        risk_free_rate = 0.03 / 252
        excess_return = daily_values['daily_return'] - risk_free_rate
        sharpe_ratio = np.sqrt(252) * excess_return.mean() / excess_return.std() if excess_return.std() != 0 else 0

        # 胜率
        profitable_trades = [t for t in self.trades if 'profit' in t and t['profit'] > 0]
        win_rate = len(profitable_trades) / len(self.trades) if self.trades else 0

        # 盈亏比
        if profitable_trades:
            avg_profit = np.mean([t['profit'] for t in profitable_trades])
            loss_trades = [t for t in self.trades if 'profit' in t and t['profit'] <= 0]
            avg_loss = np.mean([t['profit'] for t in loss_trades]) if loss_trades else 0
            profit_loss_ratio = -avg_profit / avg_loss if avg_loss != 0 else 0
        else:
            profit_loss_ratio = 0

        return BacktestResult(
            total_return=total_return,
            annual_return=annual_return,
            max_drawdown=max_drawdown,
            sharpe_ratio=sharpe_ratio,
            win_rate=win_rate,
            profit_loss_ratio=profit_loss_ratio,
            total_trades=len(self.trades),
            daily_values=daily_values,
            trades=self.trades
        )


def generate_double_ma_signal(data: pd.DataFrame, fast_period: int = 5, slow_period: int = 20) -> pd.DataFrame:
    """
    生成双均线信号

    Args:
        data: 价格数据
        fast_period: 快线周期
        slow_period: 慢线周期

    Returns:
        信号 DataFrame
    """
    df = data.copy()
    df['fast_ma'] = df['close'].rolling(fast_period).mean()
    df['slow_ma'] = df['close'].rolling(slow_period).mean()

    df['signal'] = 0
    df.loc[df['fast_ma'] > df['slow_ma'], 'signal'] = 1
    df.loc[df['fast_ma'] < df['slow_ma'], 'signal'] = -1

    return df[['date', 'signal']]
