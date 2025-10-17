# Taurus-AQuant

一个面向个人投资者的"傻瓜式"A股/ETF 算法交易项目模板：集成回测、数据、实盘网关与大模型 Agent。支持容器化部署与本地一键启动，帮助你从0到1快速搭建可交互的量化交易系统。

- **市场支持**：A股/ETF（先从日频/分钟级开始）
- **技术栈**：Python、Docker/Compose、FastAPI、Streamlit/Gradio、vn.py、rqalpha/backtrader、AkShare/Tushare、Qlib（可选）、LLM Agent（OpenAI/本地大模型可切换）
- **目标人群**：量化新手与个人开发者，既想做研究回测，也计划小额实盘灰度

---

## 功能特性

### ✨ 一键启动
- `docker compose up` 即可启动 Web UI、API 服务、回测服务与Agent服务

### 📊 回测与研究
- 内置 backtrader 与 rqalpha 两套回测管线（二选一或并行）
- 严格的中国交易日历、停牌/复权与费用模型参数位

### 📈 数据接入
- AkShare/Tushare 适配；提供数据落地与快照缓存

### 🔌 实盘预备
- 预留 vn.py 网关接入位（XTP/OpenAPI），先跑仿真/纸交易，再灰度实盘

### 🤖 LLM Agent 交互
- 策略问答、回测指令生成、风控检查清单、交易计划 JSON 输出与校验

### 🔧 可插拔组件
- 执行器（限价/TWAP/VWAP）、风控（仓位/回撤/涨跌停）、指标与因子库

---

## 目录结构

Taurus-AQuant/ ├─ apps/ │ ├─ webui/ # Streamlit/Gradio 前端 │ ├─ api/ # FastAPI：策略编排、回测触发、订单路由 │ ├─ agent/ # LLM Agent 服务（OpenAI/本地） │ └─ backtest/ # 回测服务（backtrader、rqalpha） ├─ core/ │ ├─ data/ # 数据管线：AkShare/Tushare 接口、缓存 │ ├─ signals/ # 信号与因子工程 │ ├─ execution/ # 执行器与撮合适配（仿真） │ ├─ risk/ # 风控模块（规则与校验） │ └─ brokers/ # 券商/网关适配（vn.py/XTP占位） ├─ configs/ │ ├─ settings.example.yaml │ ├─ calendar_cn.yaml │ └─ fees_cn.yaml ├─ notebooks/ # 研究与示例 ├─ docker/ │ ├─ Dockerfile.api │ ├─ Dockerfile.agent │ ├─ Dockerfile.webui │ └─ compose.yaml ├─ tests/ ├─ README.md └─ LICENSE


---

## 快速开始

### 先决条件
- 安装 Docker 与 Docker Compose
- 申请数据源 Token（如 Tushare，可选）
- 如需云端 LLM，准备 API Key；也支持本地大模型（如 ollama/LM Studio）

### 一键启动（容器化）

```bash
cd Taurus-AQuant/docker
docker compose up -d
启动后：

Web UI: http://localhost:8501
API: http://localhost:8000/docs
Agent: http://localhost:8080 (内部通信为主)
本地开发（不使用容器）

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export TUSHARE_TOKEN=xxx
export OPENAI_API_KEY=xxx   # 如使用云端 LLM
uvicorn apps.api.main:app --reload --port 8000
streamlit run apps/webui/Home.py --server.port 8501
典型工作流

1. 数据准备

在 Web UI 选择标的与区间，触发数据下载与本地缓存（AkShare/Tushare）
2. 策略生成与回测

在"Agent对话"中描述策略想法，Agent 生成策略 JSON/代码草案
选择回测引擎（backtrader/rqalpha），一键回测，输出图表与指标（年化、夏普、最大回撤、换手、成本等）
3. 风控与执行模拟

根据风控规则校验：涨跌停、仓位上限、集中度、滑点与费率
使用模拟执行器（限价/TWAP）进行成交质量评估（实现价差/冲击成本）
4. 实盘灰度（可选）

配置 vn.py 网关（券商测试环境/XTP），在 Paper Trading 模式下进行仿真
逐步切换小额实盘，开启告警与熔断
LLM Agent 设计要点

角色划分

Researcher：信息整合/因子建议
Strategist：生成策略 JSON（schema 固化）
RiskOfficer：规则检查与约束报告
Trader：生成订单计划（仅结构化输出）
输出 Schema（示例）

{
  "signal": [
    {
      "ticker": "600519.SH",
      "side": "buy",
      "confidence": 0.72,
      "horizon": "20d"
    }
  ],
  "order_plan": [
    {
      "ticker": "510300.SH",
      "type": "limit",
      "limit_price": 3.12,
      "qty": 1000,
      "tif": "day"
    }
  ],
  "risk": {
    "max_position": 0.3,
    "drawdown_stop": 0.1,
    "limit_up_down_check": true
  }
}
守门人

所有 Agent 输出进入 rule-based 校验器，再交由回测/执行层处理
配置与环境变量

configs/settings.yaml

market: CN_A
data:
  provider: "akshare"  # 或 "tushare"
  token: "..."
backtester: "backtrader"  # 或 "rqalpha"
llm:
  provider: "openai"  # 或 "ollama"
  model: "gpt-4o-mini"  # 或 "qwen2.5"
  api_key_env: "OPENAI_API_KEY"
broker:
  provider: "vnpy"
  gateway: "xtp"
  paper: true
关键环境变量

TUSHARE_TOKEN
OPENAI_API_KEY 或 OLLAMA_BASE_URL
示例命令

拉取沪深300历史数据并回测动量策略

curl -X POST http://localhost:8000/backtest/run \
  -H "Content-Type: application/json" \
  -d '{
    "universe": "HS300",
    "strategy": "momentum_ma",
    "start": "2018-01-01",
    "end": "2024-12-31"
  }'
通过 Agent 生成策略参数并回测

curl -X POST http://localhost:8000/agent/strategy \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "为沪深300做一个MA(10/60)+波动目标仓位策略，控制最大回撤10%"
  }'
开发路线图（Roadmap）

v0.1（当前）
backtrader 管线、AkShare 数据、基础指标与费用/滑点模型、简易Agent对话
v0.2
rqalpha 接入、滚动回测（walk-forward）、策略/实验追踪（MLflow）
v0.3
vn.py 仿真账户、风控熔断/告警、订单状态一致性检查
v0.4
Qlib 数据/因子流水线、LightGBM/线下训练与在线推理
v0.5
实盘灰度工具包：小额资金管理、异常恢复、成交质量报表
⚠️ 合规与风险声明

本项目仅用于学习与研究，不构成任何投资建议。
自动化交易存在技术与市场风险。实盘前请充分仿真，并遵守券商与交易所规则。
使用任何第三方数据/接口需遵从其授权与使用条款。
许可证

MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

贡献

欢迎通过 Issue/PR 提交需求与改进。建议遵循：

提交前跑通 tests 与 lint
附带最小复现示例
对公共API与配置项补充文档
联系方式

Issues: GitHub Issues
Discussions: GitHub Discussions
Happy Trading! 📈🚀
