# 系统架构设计

**Taurus-AQuant 技术架构与模块设计**

---

## 文档信息

| 项目 | 内容 |
|------|------|
| **项目名称** | Taurus-AQuant |
| **架构版本** | v1.0 |
| **文档状态** | 草稿 |
| **创建日期** | 2026-03-02 |
| **最后更新** | 2026-03-02 |
| **架构师** | 项目团队 |
| **相关文档** | [产品需求文档](PRD.md) · [路线图](ROADMAP.md) |

---

## 一、架构概览

### 1.1 系统架构图

```
┌─────────────────────────────────────────────────────────────────────┐
│                           用户层                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  Web Browser │  │  API Client  │  │  CLI Tool    │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
└─────────────────────────────────────────────────────────────────────┘
                                 ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        接入层 (Nginx)                                │
│                    负载均衡 + 反向代理                                │
└─────────────────────────────────────────────────────────────────────┘
                                 ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        应用层 (Docker)                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  Web UI      │  │  API 服务    │  │  Agent 服务   │              │
│  │  (Streamlit) │  │  (FastAPI)   │  │  (LLM Agent) │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
└─────────────────────────────────────────────────────────────────────┘
                                 ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        核心服务层                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ 数据服务     │  │ 回测引擎     │  │ 交易引擎     │              │
│  │ DataService  │  │ Backtest     │  │ Trading      │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ 风控系统     │  │ 策略引擎     │  │ 执行器       │              │
│  │ RiskControl  │  │ Strategy     │  │ Executor     │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
└─────────────────────────────────────────────────────────────────────┘
                                 ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        基础设施层                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ PostgreSQL   │  │   Redis      │  │ 文件存储     │              │
│  │ (数据存储)   │  │  (缓存)      │  │ (日志/报告)  │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ Tushare API  │  │ OpenAI API   │  │ 券商接口     │              │
│  │ (数据源)     │  │ (LLM)        │  │ (XTP/etc)    │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 核心设计原则

1. **模块化设计**
   - 高内聚、低耦合
   - 每个模块独立职责，易于测试和维护

2. **可插拔架构**
   - 数据源、回测引擎、券商接口、LLM 模型都可插拔
   - 通过适配器模式统一接口

3. **异步优先**
   - 使用异步 I/O 提升性能
   - 长时间任务（回测、数据更新）使用后台任务队列

4. **配置驱动**
   - 通过配置文件控制行为，减少硬编码
   - 支持多环境配置（开发、测试、生产）

5. **安全第一**
   - 敏感信息加密存储
   - API 鉴权
   - 实盘操作多重确认

6. **可观测性**
   - 完整的日志记录
   - 性能监控
   - 异常告警

---

## 二、核心模块设计

### 2.1 数据服务模块 (DataService)

#### 2.1.1 模块概述

负责数据获取、存储、缓存、更新、导出等功能。

#### 2.1.2 核心类设计

```python
# src/data/data_service.py

from abc import ABC, abstractmethod
from typing import List, Optional, Dict
import pandas as pd
from datetime import datetime

class DataSourceAdapter(ABC):
    """数据源适配器抽象基类"""

    @abstractmethod
    def get_daily_data(
        self,
        symbol: str,
        start_date: str,
        end_date: str
    ) -> pd.DataFrame:
        """获取日线数据"""
        pass

    @abstractmethod
    def get_minute_data(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        freq: str = '1min'
    ) -> pd.DataFrame:
        """获取分钟线数据"""
        pass

    @abstractmethod
    def get_trade_calendar(
        self,
        exchange: str = 'SSE',
        start_date: str = None,
        end_date: str = None
    ) -> pd.DataFrame:
        """获取交易日历"""
        pass


class TushareAdapter(DataSourceAdapter):
    """Tushare 数据源适配器"""

    def __init__(self, token: str):
        self.token = token
        # TODO: 初始化 Tushare Pro API
        pass

    def get_daily_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        # TODO: 调用 Tushare API
        pass

    def get_minute_data(self, symbol: str, start_date: str, end_date: str, freq: str = '1min') -> pd.DataFrame:
        # TODO: 调用 Tushare API
        pass

    def get_trade_calendar(self, exchange: str = 'SSE', start_date: str = None, end_date: str = None) -> pd.DataFrame:
        # TODO: 调用 Tushare API
        pass


class AkShareAdapter(DataSourceAdapter):
    """AkShare 数据源适配器"""

    def get_daily_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        # TODO: 调用 AkShare API
        pass

    def get_minute_data(self, symbol: str, start_date: str, end_date: str, freq: str = '1min') -> pd.DataFrame:
        # TODO: 调用 AkShare API
        pass

    def get_trade_calendar(self, exchange: str = 'SSE', start_date: str = None, end_date: str = None) -> pd.DataFrame:
        # TODO: 调用 AkShare API
        pass


class DataCache:
    """数据缓存层"""

    def __init__(self, redis_client):
        self.redis = redis_client

    def get(self, key: str) -> Optional[pd.DataFrame]:
        """从缓存获取数据"""
        # TODO: 实现缓存读取
        pass

    def set(self, key: str, data: pd.DataFrame, expire: int = 3600):
        """设置缓存"""
        # TODO: 实现缓存写入
        pass


class DataQualityChecker:
    """数据质量检查器"""

    @staticmethod
    def check_missing_values(df: pd.DataFrame) -> Dict:
        """检查缺失值"""
        # TODO: 实现缺失值检查
        pass

    @staticmethod
    def check_outliers(df: pd.DataFrame) -> Dict:
        """检查异常值"""
        # TODO: 实现异常值检查
        pass


class DataService:
    """数据服务主类"""

    def __init__(
        self,
        data_source: DataSourceAdapter,
        cache: DataCache,
        db_connector
    ):
        self.data_source = data_source
        self.cache = cache
        self.db = db_connector

    def get_data(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        freq: str = 'daily',
        use_cache: bool = True
    ) -> pd.DataFrame:
        """获取数据（优先从缓存）"""
        # TODO: 实现数据获取逻辑
        # 1. 检查缓存
        # 2. 如果缓存命中，返回数据
        # 3. 如果缓存未命中，从数据源获取
        # 4. 检查数据质量
        # 5. 存储到数据库
        # 6. 更新缓存
        pass

    def update_daily(self):
        """每日自动更新数据"""
        # TODO: 实现自动更新逻辑
        pass
```

#### 2.1.3 数据流

```
用户请求 → DataService.get_data()
    ↓
检查缓存 (Redis)
    ↓ (缓存未命中)
调用数据源适配器 (Tushare/AkShare)
    ↓
数据质量检查 (DataQualityChecker)
    ↓
存储到数据库 (PostgreSQL)
    ↓
更新缓存 (Redis)
    ↓
返回数据给用户
```

---

### 2.2 回测引擎模块 (BacktestEngine)

#### 2.2.1 模块概述

提供策略回测、绩效分析、报告生成等功能。

#### 2.2.2 核心类设计

```python
# src/backtest/backtest_engine.py

from abc import ABC, abstractmethod
from typing import Dict, List
import pandas as pd
from dataclasses import dataclass

@dataclass
class BacktestConfig:
    """回测配置"""
    symbol: str
    start_date: str
    end_date: str
    initial_cash: float
    commission: float = 0.0003  # 佣金率
    stamp_tax: float = 0.001    # 印花税
    slippage: float = 0.0       # 滑点
    benchmark: str = '000300.SH'  # 基准指数


@dataclass
class BacktestResult:
    """回测结果"""
    total_return: float      # 总收益率
    annual_return: float     # 年化收益率
    max_drawdown: float      # 最大回撤
    sharpe_ratio: float      # 夏普比率
    win_rate: float          # 胜率
    profit_loss_ratio: float # 盈亏比
    trades: List[Dict]       # 交易记录
    daily_values: pd.DataFrame  # 每日资产价值


class BacktestEngineAdapter(ABC):
    """回测引擎适配器抽象基类"""

    @abstractmethod
    def run_backtest(
        self,
        strategy,
        config: BacktestConfig,
        data: pd.DataFrame
    ) -> BacktestResult:
        """执行回测"""
        pass


class BacktraderAdapter(BacktestEngineAdapter):
    """Backtrader 适配器"""

    def run_backtest(
        self,
        strategy,
        config: BacktestConfig,
        data: pd.DataFrame
    ) -> BacktestResult:
        # TODO: 实现 Backtrader 回测逻辑
        pass


class RqalphaAdapter(BacktestEngineAdapter):
    """Rqalpha 适配器"""

    def run_backtest(
        self,
        strategy,
        config: BacktestConfig,
        data: pd.DataFrame
    ) -> BacktestResult:
        # TODO: 实现 Rqalpha 回测逻辑
        pass


class PerformanceAnalyzer:
    """绩效分析器"""

    @staticmethod
    def calculate_metrics(daily_values: pd.DataFrame) -> Dict:
        """计算绩效指标"""
        # TODO: 实现绩效指标计算
        # - 年化收益率
        # - 最大回撤
        # - 夏普比率
        # - 胜率
        # - 盈亏比
        # - Alpha
        # - Beta
        pass


class BacktestService:
    """回测服务主类"""

    def __init__(
        self,
        engine: BacktestEngineAdapter,
        data_service: DataService
    ):
        self.engine = engine
        self.data_service = data_service

    def run(
        self,
        strategy,
        config: BacktestConfig
    ) -> BacktestResult:
        """执行回测"""
        # TODO: 实现回测流程
        # 1. 获取数据
        # 2. 调用回测引擎
        # 3. 计算绩效指标
        # 4. 生成报告
        pass

    def generate_report(
        self,
        result: BacktestResult,
        output_format: str = 'html'
    ) -> str:
        """生成回测报告"""
        # TODO: 实现报告生成
        pass
```

---

### 2.3 LLM Agent 模块 (AgentService)

#### 2.3.1 模块概述

集成大语言模型，支持自然语言交互、策略生成、风险分析等功能。

#### 2.3.2 架构图

```
┌──────────────────────────────────────────────────────┐
│                  用户对话界面                         │
└──────────────────────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────┐
│               Prompt 管理层                          │
│  ┌──────────────┬──────────────┬──────────────┐    │
│  │ 策略生成     │ 风险分析     │ 市场解读     │    │
│  └──────────────┴──────────────┴──────────────┘    │
└──────────────────────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────┐
│               LLM 引擎适配器                         │
│  ┌──────────────┬──────────────┬──────────────┐    │
│  │ OpenAI GPT   │ Claude       │ Ollama       │    │
│  └──────────────┴──────────────┴──────────────┘    │
└──────────────────────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────┐
│               结果处理层                             │
│  ┌──────────────┬──────────────┬──────────────┐    │
│  │ 代码校验     │ 代码执行     │ 结果格式化   │    │
│  └──────────────┴──────────────┴──────────────┘    │
└──────────────────────────────────────────────────────┘
```

#### 2.3.3 核心类设计

```python
# src/agent/agent_service.py

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import openai

class LLMAdapter(ABC):
    """LLM 适配器抽象基类"""

    @abstractmethod
    def chat(
        self,
        messages: List[Dict],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """对话接口"""
        pass


class OpenAIAdapter(LLMAdapter):
    """OpenAI GPT 适配器"""

    def __init__(self, api_key: str, model: str = 'gpt-4'):
        self.api_key = api_key
        self.model = model
        openai.api_key = api_key

    def chat(
        self,
        messages: List[Dict],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        # TODO: 调用 OpenAI API
        pass


class ClaudeAdapter(LLMAdapter):
    """Claude 适配器"""

    def chat(
        self,
        messages: List[Dict],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        # TODO: 调用 Claude API
        pass


class OllamaAdapter(LLMAdapter):
    """Ollama 本地 LLM 适配器"""

    def __init__(self, host: str = 'http://localhost:11434', model: str = 'llama2'):
        self.host = host
        self.model = model

    def chat(
        self,
        messages: List[Dict],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        # TODO: 调用 Ollama API
        pass


class PromptManager:
    """Prompt 模板管理器"""

    @staticmethod
    def get_strategy_generation_prompt(user_input: str) -> str:
        """获取策略生成 Prompt"""
        # TODO: 返回 Prompt 模板
        pass

    @staticmethod
    def get_risk_analysis_prompt(strategy_code: str) -> str:
        """获取风险分析 Prompt"""
        # TODO: 返回 Prompt 模板
        pass


class CodeValidator:
    """代码校验器"""

    @staticmethod
    def validate_python_code(code: str) -> Dict:
        """校验 Python 代码"""
        # TODO: 实现代码校验
        # - 语法检查
        # - 安全检查
        # - 依赖检查
        pass


class AgentService:
    """Agent 服务主类"""

    def __init__(self, llm_adapter: LLMAdapter):
        self.llm = llm_adapter
        self.prompt_manager = PromptManager()
        self.validator = CodeValidator()

    def chat(self, user_input: str, context: Dict = None) -> str:
        """对话接口"""
        # TODO: 实现对话逻辑
        pass

    def generate_strategy(self, description: str) -> Dict:
        """生成策略代码"""
        # TODO: 实现策略生成
        # 1. 构建 Prompt
        # 2. 调用 LLM
        # 3. 校验代码
        # 4. 返回结果
        pass

    def analyze_risk(self, strategy_code: str) -> Dict:
        """分析策略风险"""
        # TODO: 实现风险分析
        pass
```

---

### 2.4 实盘交易模块 (TradingService)

#### 2.4.1 模块概述

支持仿真交易和实盘交易，包括订单管理、持仓管理、执行器等功能。

#### 2.4.2 核心类设计

```python
# src/trading/trading_service.py

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

class OrderStatus(Enum):
    """订单状态"""
    PENDING = 'pending'
    SUBMITTED = 'submitted'
    FILLED = 'filled'
    CANCELLED = 'cancelled'
    REJECTED = 'rejected'


class OrderType(Enum):
    """订单类型"""
    MARKET = 'market'
    LIMIT = 'limit'


@dataclass
class Order:
    """订单"""
    order_id: str
    symbol: str
    side: str  # 'buy' or 'sell'
    quantity: int
    price: Optional[float]
    order_type: OrderType
    status: OrderStatus
    created_at: datetime
    updated_at: datetime


@dataclass
class Position:
    """持仓"""
    symbol: str
    quantity: int
    avg_cost: float
    current_price: float
    market_value: float
    profit_loss: float
    profit_loss_pct: float


class BrokerGateway(ABC):
    """券商网关抽象基类"""

    @abstractmethod
    def connect(self):
        """连接券商"""
        pass

    @abstractmethod
    def submit_order(self, order: Order) -> str:
        """提交订单"""
        pass

    @abstractmethod
    def cancel_order(self, order_id: str):
        """取消订单"""
        pass

    @abstractmethod
    def get_positions(self) -> List[Position]:
        """查询持仓"""
        pass

    @abstractmethod
    def get_account_info(self) -> Dict:
        """查询账户信息"""
        pass


class XTPGateway(BrokerGateway):
    """XTP 券商网关"""

    def connect(self):
        # TODO: 实现 XTP 连接
        pass

    def submit_order(self, order: Order) -> str:
        # TODO: 实现订单提交
        pass

    def cancel_order(self, order_id: str):
        # TODO: 实现订单取消
        pass

    def get_positions(self) -> List[Position]:
        # TODO: 实现持仓查询
        pass

    def get_account_info(self) -> Dict:
        # TODO: 实现账户查询
        pass


class OrderManager:
    """订单管理器"""

    def __init__(self):
        self.orders: Dict[str, Order] = {}

    def create_order(self, **kwargs) -> Order:
        """创建订单"""
        # TODO: 实现订单创建
        pass

    def update_order_status(self, order_id: str, status: OrderStatus):
        """更新订单状态"""
        # TODO: 实现状态更新
        pass


class TradingService:
    """交易服务主类"""

    def __init__(
        self,
        gateway: BrokerGateway,
        risk_checker: 'RiskChecker'
    ):
        self.gateway = gateway
        self.risk_checker = risk_checker
        self.order_manager = OrderManager()

    def place_order(self, **kwargs) -> Order:
        """下单"""
        # TODO: 实现下单流程
        # 1. 创建订单
        # 2. 风控检查
        # 3. 提交到券商
        # 4. 更新状态
        pass

    def get_positions(self) -> List[Position]:
        """查询持仓"""
        # TODO: 实现持仓查询
        pass
```

---

### 2.5 风控系统模块 (RiskControl)

#### 2.5.1 模块概述

提供多层次的风险控制，包括仓位控制、频率限制、止损止盈等。

#### 2.5.2 核心类设计

```python
# src/risk/risk_control.py

from abc import ABC, abstractmethod
from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class RiskCheckResult:
    """风控检查结果"""
    passed: bool
    reason: str
    risk_level: str  # 'low', 'medium', 'high'


class RiskRule(ABC):
    """风控规则抽象基类"""

    @abstractmethod
    def check(self, context: Dict) -> RiskCheckResult:
        """检查风控规则"""
        pass


class PositionLimitRule(RiskRule):
    """仓位限制规则"""

    def __init__(self, max_position_pct: float = 0.3):
        self.max_position_pct = max_position_pct

    def check(self, context: Dict) -> RiskCheckResult:
        # TODO: 实现仓位限制检查
        pass


class FrequencyLimitRule(RiskRule):
    """交易频率限制规则"""

    def __init__(self, max_trades_per_day: int = 10):
        self.max_trades_per_day = max_trades_per_day

    def check(self, context: Dict) -> RiskCheckResult:
        # TODO: 实现频率限制检查
        pass


class StopLossRule(RiskRule):
    """止损规则"""

    def __init__(self, stop_loss_pct: float = -0.05):
        self.stop_loss_pct = stop_loss_pct

    def check(self, context: Dict) -> RiskCheckResult:
        # TODO: 实现止损检查
        pass


class BlacklistRule(RiskRule):
    """黑名单规则"""

    def __init__(self, blacklist: list):
        self.blacklist = blacklist

    def check(self, context: Dict) -> RiskCheckResult:
        # TODO: 实现黑名单检查
        pass


class RiskChecker:
    """风控检查器"""

    def __init__(self, rules: list):
        self.rules = rules

    def check_all(self, context: Dict) -> RiskCheckResult:
        """执行所有风控检查"""
        # TODO: 实现风控检查逻辑
        pass
```

---

## 三、数据流设计

### 3.1 回测数据流

```
┌──────────────┐
│  用户配置    │
│ (Web UI/API) │
└──────────────┘
       ↓
┌──────────────┐
│ Backtest     │
│ Service      │
└──────────────┘
       ↓
┌──────────────┐
│ Data Service │
│ (获取数据)    │
└──────────────┘
       ↓
┌──────────────┐
│ Backtest     │
│ Engine       │
│ (执行回测)    │
└──────────────┘
       ↓
┌──────────────┐
│ Performance  │
│ Analyzer     │
│ (计算指标)    │
└──────────────┘
       ↓
┌──────────────┐
│ Report       │
│ Generator    │
│ (生成报告)    │
└──────────────┘
       ↓
┌──────────────┐
│ 返回给用户   │
└──────────────┘
```

### 3.2 实盘交易数据流

```
┌──────────────┐
│  策略信号    │
└──────────────┘
       ↓
┌──────────────┐
│ Trading      │
│ Service      │
│ (创建订单)    │
└──────────────┘
       ↓
┌──────────────┐
│ Risk Checker │
│ (风控检查)    │
└──────────────┘
       ↓ (通过)
┌──────────────┐
│ Executor     │
│ (执行器)      │
└──────────────┘
       ↓
┌──────────────┐
│ Broker       │
│ Gateway      │
│ (券商接口)    │
└──────────────┘
       ↓
┌──────────────┐
│ 更新订单状态 │
└──────────────┘
```

---

## 四、部署架构

### 4.1 Docker 容器编排

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Web UI
  web:
    build: ./src/ui
    ports:
      - "8501:8501"
    depends_on:
      - api
      - postgres
      - redis
    environment:
      - API_URL=http://api:8000
      - DATABASE_URL=postgresql://taurus:taurus123@postgres:5432/taurus_aquant
      - REDIS_URL=redis://redis:6379

  # API 服务
  api:
    build: ./src/api
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
    environment:
      - DATABASE_URL=postgresql://taurus:taurus123@postgres:5432/taurus_aquant
      - REDIS_URL=redis://redis:6379
      - TUSHARE_TOKEN=${TUSHARE_TOKEN}
      - OPENAI_API_KEY=${OPENAI_API_KEY}

  # PostgreSQL 数据库
  postgres:
    image: postgres:15
    environment:
      - POSTGRES_USER=taurus
      - POSTGRES_PASSWORD=taurus123
      - POSTGRES_DB=taurus_aquant
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  # Redis 缓存
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"

volumes:
  postgres_data:
  redis_data:
```

### 4.2 目录结构

```
taurus-Aquant/
├── src/                        # 源代码
│   ├── api/                    # FastAPI 服务
│   │   ├── main.py
│   │   ├── routers/
│   │   │   ├── data.py
│   │   │   ├── backtest.py
│   │   │   ├── strategy.py
│   │   │   ├── agent.py
│   │   │   └── trading.py
│   │   └── models/
│   ├── backtest/               # 回测引擎
│   │   ├── backtest_engine.py
│   │   ├── performance.py
│   │   └── report.py
│   ├── data/                   # 数据服务
│   │   ├── data_service.py
│   │   ├── adapters/
│   │   │   ├── tushare_adapter.py
│   │   │   └── akshare_adapter.py
│   │   └── models/
│   ├── agent/                  # LLM Agent
│   │   ├── agent_service.py
│   │   ├── llm_adapters/
│   │   │   ├── openai_adapter.py
│   │   │   ├── claude_adapter.py
│   │   │   └── ollama_adapter.py
│   │   └── prompts/
│   ├── trading/                # 交易网关
│   │   ├── trading_service.py
│   │   ├── broker_gateways/
│   │   │   └── xtp_gateway.py
│   │   └── executor/
│   ├── risk/                   # 风控系统
│   │   ├── risk_control.py
│   │   └── rules/
│   ├── ui/                     # Web UI
│   │   ├── app.py
│   │   ├── pages/
│   │   │   ├── home.py
│   │   │   ├── strategy.py
│   │   │   ├── backtest.py
│   │   │   └── trading.py
│   │   └── components/
│   └── utils/                  # 工具函数
│       ├── logger.py
│       ├── config.py
│       └── helpers.py
├── tests/                      # 测试代码
│   ├── test_data/
│   ├── test_backtest/
│   ├── test_agent/
│   └── test_trading/
├── configs/                    # 配置文件
│   ├── dev.yaml
│   ├── prod.yaml
│   └── test.yaml
├── scripts/                    # 工具脚本
│   ├── update_data.py
│   └── init_db.py
├── docs/                       # 文档
├── requirements.txt            # Python 依赖
├── Dockerfile                  # Docker 镜像
├── docker-compose.yml          # Docker 编排
└── README.md                   # 项目说明
```

---

## 五、技术选型理由

### 5.1 FastAPI vs Flask

**选择 FastAPI 的理由**：
1. **性能更高**：基于 Starlette 和 Pydantic，性能接近 Node.js
2. **异步支持**：原生支持 async/await，适合 I/O 密集型任务
3. **自动文档**：自动生成 Swagger 文档，减少维护成本
4. **类型提示**：强制类型提示，代码更健壮

### 5.2 Backtrader vs Rqalpha

**支持两者的理由**：
- **Backtrader**：社区活跃，文档完善，适合快速原型开发
- **Rqalpha**：中国市场支持更好，更专业的绩效分析

**策略**：通过适配器模式支持两者，用户可以根据需求选择。

### 5.3 vn.py 的优势

**选择 vn.py 的理由**：
1. **券商支持**：支持国内主流券商接口（XTP、CTP 等）
2. **成熟稳定**：经过大量实盘验证
3. **社区活跃**：国内最大的开源量化社区之一
4. **功能完善**：覆盖回测、仿真、实盘全流程

### 5.4 Streamlit vs Gradio

**选择 Streamlit 的理由**：
1. **易用性**：Python 代码快速生成 UI，无需前端知识
2. **生态丰富**：大量第三方组件
3. **性能优秀**：自动缓存，响应快速
4. **适合数据应用**：天然适合数据可视化和分析应用

---

## 六、性能优化策略

### 6.1 数据缓存策略

1. **Redis 多层缓存**
   - 热点数据缓存（如最新行情）
   - 查询结果缓存（如回测结果）
   - 缓存过期时间：根据数据更新频率设置

2. **数据库优化**
   - 建立合适的索引（symbol + date）
   - 分区表（按年份分区）
   - 定期清理历史数据

### 6.2 回测性能优化

1. **向量化计算**
   - 使用 Pandas/Numpy 向量化操作
   - 避免逐行循环

2. **并行化**
   - 多策略并行回测
   - 参数优化并行化

3. **增量计算**
   - 增量更新回测结果
   - 避免重复计算

### 6.3 API 性能优化

1. **异步处理**
   - 长时间任务使用后台任务队列（Celery）
   - API 立即返回任务 ID，前端轮询结果

2. **连接池**
   - 数据库连接池
   - Redis 连接池

---

## 七、安全性设计

### 7.1 API 鉴权

```python
# 使用 JWT Token 鉴权
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_current_user(token: str = Depends(security)):
    # TODO: 实现 JWT 验证
    pass
```

### 7.2 敏感信息保护

1. **环境变量**：API Key 等敏感信息通过环境变量传入
2. **加密存储**：数据库中的敏感信息加密存储
3. **不记录日志**：敏感信息不记录到日志

### 7.3 实盘安全

1. **多重确认**：实盘操作需要二次确认
2. **风控前置**：所有订单必须通过风控检查
3. **人工审核**：大额交易可配置人工审核

---

## 八、监控与运维

### 8.1 日志系统

```python
# 使用 Python logging 模块
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
```

### 8.2 健康检查

```python
# FastAPI 健康检查接口
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": check_database(),
        "redis": check_redis(),
        "timestamp": datetime.now().isoformat()
    }
```

### 8.3 性能监控

- **Prometheus**：指标采集
- **Grafana**：可视化监控
- **AlertManager**：告警通知

---

## 九、扩展点设计

### 9.1 数据源扩展

实现 `DataSourceAdapter` 接口即可添加新数据源。

### 9.2 回测引擎扩展

实现 `BacktestEngineAdapter` 接口即可添加新引擎。

### 9.3 LLM 扩展

实现 `LLMAdapter` 接口即可添加新模型。

### 9.4 券商接口扩展

实现 `BrokerGateway` 接口即可添加新券商。

### 9.5 风控规则扩展

实现 `RiskRule` 接口即可添加新规则。

---

**文档版本**：v1.0
**最后更新**：2026-03-02
**维护者**：项目团队
