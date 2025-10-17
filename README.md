# Taurus-AQuant

## 开发中...

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

