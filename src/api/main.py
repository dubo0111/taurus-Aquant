"""
FastAPI 应用主模块
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.utils.config import settings
from src.utils.logger import logger
from src.data.data_service import DataService
from src.backtest.backtest_engine import BacktestEngine, BacktestConfig, generate_double_ma_signal

# 导入路由
from .routers import agent as agent_router


# 创建 FastAPI 应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI 驱动的 A股/ETF 算法交易平台",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(agent_router.router)


# ========== 请求/响应模型 ==========

class HealthResponse(BaseModel):
    """健康检查响应"""
    status: str
    app_name: str
    version: str
    timestamp: str


class BacktestRequest(BaseModel):
    """回测请求"""
    symbol: str
    start_date: str
    end_date: str
    initial_cash: float = 100000.0
    strategy: str = "double_ma"
    params: Optional[dict] = {}


class BacktestResponse(BaseModel):
    """回测响应"""
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    profit_loss_ratio: float
    total_trades: int
    trades: List[dict]


# ========== API 路由 ==========

@app.get("/", tags=["Root"])
async def root():
    """根路径"""
    return {
        "message": f"欢迎来到 {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """健康检查"""
    return HealthResponse(
        status="healthy",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        timestamp=datetime.now().isoformat()
    )


@app.post("/api/backtest/run", response_model=BacktestResponse, tags=["Backtest"])
async def run_backtest(request: BacktestRequest):
    """
    执行回测

    Args:
        request: 回测请求参数

    Returns:
        回测结果
    """
    try:
        logger.info(f"收到回测请求: {request.symbol}, {request.start_date} - {request.end_date}")

        # 获取数据（这里需要 TUSHARE_TOKEN）
        # data_service = DataService()
        # data = data_service.get_daily_data(request.symbol, request.start_date, request.end_date)

        # 临时：返回模拟数据
        logger.warning("使用模拟数据（TUSHARE_TOKEN 未配置）")

        # 创建回测配置
        config = BacktestConfig(
            symbol=request.symbol,
            start_date=request.start_date,
            end_date=request.end_date,
            initial_cash=request.initial_cash
        )

        # 创建模拟数据
        import pandas as pd
        import numpy as np
        from datetime import timedelta

        dates = pd.date_range(start=request.start_date, end=request.end_date, freq='D')
        np.random.seed(42)
        prices = [10.0]
        for i in range(1, len(dates)):
            change = np.random.randn() * 0.02
            prices.append(prices[-1] * (1 + change))

        data = pd.DataFrame({
            'date': dates,
            'open': prices,
            'high': [p * 1.02 for p in prices],
            'low': [p * 0.98 for p in prices],
            'close': prices,
            'volume': [1000000] * len(dates)
        })

        # 生成信号
        if request.strategy == "double_ma":
            fast_period = request.params.get('fast_period', 5)
            slow_period = request.params.get('slow_period', 20)
            signals = generate_double_ma_signal(data, fast_period, slow_period)
        else:
            raise HTTPException(status_code=400, detail=f"未知策略: {request.strategy}")

        # 运行回测
        engine = BacktestEngine(config)
        result = engine.run(data, signals)

        return BacktestResponse(
            total_return=result.total_return,
            annual_return=result.annual_return,
            max_drawdown=result.max_drawdown,
            sharpe_ratio=result.sharpe_ratio,
            win_rate=result.win_rate,
            profit_loss_ratio=result.profit_loss_ratio,
            total_trades=result.total_trades,
            trades=result.trades
        )

    except Exception as e:
        logger.error(f"回测失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== 启动事件 ==========

@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    logger.info(f"{settings.APP_NAME} v{settings.APP_VERSION} 启动")
    logger.info(f"API 文档: http://{settings.API_HOST}:{settings.API_PORT}/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logger.info(f"{settings.APP_NAME} 关闭")


# ========== 主函数 ==========

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
        log_level="info"
    )
