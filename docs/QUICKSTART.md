# 快速入门指南

**15 分钟快速体验 Taurus-AQuant 算法交易系统**

---

## 📋 前置条件

### 必需环境

1. **Docker Desktop**
   - [下载 Docker Desktop](https://www.docker.com/products/docker-desktop/)
   - 支持 Windows / macOS / Linux
   - 版本要求：20.10+

2. **系统资源**
   - 内存：至少 4GB RAM（推荐 8GB+）
   - 磁盘：至少 10GB 可用空间
   - CPU：双核及以上

3. **API Key**
   - **Tushare Token**（必需）：[免费注册](https://tushare.pro/register)
   - **OpenAI API Key**（可选）：用于 LLM Agent 功能

### 可选环境

- **Python 3.10+**：用于本地开发或脚本执行
- **Git**：用于克隆项目

---

## 🚀 3 步启动

### 步骤 1：克隆项目

```bash
# 使用 Git 克隆
git clone https://github.com/yourusername/taurus-Aquant.git
cd taurus-Aquant

# 或者直接下载 ZIP 压缩包
# wget https://github.com/yourusername/taurus-Aquant/archive/refs/heads/main.zip
# unzip main.zip
# cd taurus-Aquant-main
```

### 步骤 2：配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件（选择你喜欢的编辑器）
nano .env
# 或
vim .env
# 或
code .env
```

**必需配置项**：

```bash
# Tushare 数据源配置（必需）
TUSHARE_TOKEN=your_tushare_token_here

# 数据库配置（默认即可）
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=taurus_aquant
POSTGRES_USER=taurus
POSTGRES_PASSWORD=taurus123

# Redis 配置（默认即可）
REDIS_HOST=redis
REDIS_PORT=6379
```

**可选配置项**：

```bash
# OpenAI API 配置（可选，用于 LLM Agent）
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4

# 本地 LLM 配置（可选）
OLLAMA_HOST=http://ollama:11434
OLLAMA_MODEL=llama2
```

### 步骤 3：启动服务

```bash
# 启动所有服务（首次启动会自动构建镜像，需要 5-10 分钟）
docker compose up -d

# 查看服务状态
docker compose ps

# 查看日志
docker compose logs -f
```

**服务启动成功标志**：

```bash
# 所有服务状态为 "healthy"
NAME                STATUS              PORTS
taurus-web          Up (healthy)        0.0.0.0:8501->8501/tcp
taurus-api          Up (healthy)        0.0.0.0:8000->8000/tcp
taurus-postgres     Up (healthy)        5432/tcp
taurus-redis        Up (healthy)        6379/tcp
```

---

## 🌐 访问服务

### Web UI

访问 http://localhost:8501 进入 Streamlit Web 界面。

**主要功能**：
- **首页**：系统概览、服务状态
- **策略管理**：创建、编辑、删除策略
- **回测中心**：配置回测参数、执行回测
- **结果分析**：查看回测报告、绩效指标
- **实盘监控**：查看实盘交易状态（需配置券商接口）

### API 文档

访问 http://localhost:8000/docs 查看 FastAPI 自动生成的 Swagger API 文档。

**主要接口**：
- `/api/data/` - 数据管理接口
- `/api/backtest/` - 回测执行接口
- `/api/strategy/` - 策略管理接口
- `/api/agent/` - LLM Agent 交互接口

---

## 📊 第一个回测示例

### 使用内置策略

我们提供了一个简单的双均线策略示例。

#### 方法 1：通过 Web UI

1. 打开 Web UI：http://localhost:8501
2. 进入 **策略管理** 页面
3. 选择内置策略 **"双均线策略"**
4. 配置回测参数：
   - **股票代码**：`000001.SZ`（平安银行）
   - **开始日期**：`2023-01-01`
   - **结束日期**：`2023-12-31`
   - **初始资金**：`100000`（10 万元）
   - **快线周期**：`5`
   - **慢线周期**：`20`
5. 点击 **开始回测**
6. 等待回测完成（通常 10-30 秒）
7. 查看回测报告：
   - 年化收益率
   - 最大回撤
   - 夏普比率
   - 收益曲线图
   - 持仓明细

#### 方法 2：通过 API

```bash
# 调用回测 API
curl -X POST "http://localhost:8000/api/backtest/run" \
  -H "Content-Type: application/json" \
  -d '{
    "strategy": "double_ma",
    "symbol": "000001.SZ",
    "start_date": "2023-01-01",
    "end_date": "2023-12-31",
    "initial_cash": 100000,
    "params": {
      "fast_period": 5,
      "slow_period": 20
    }
  }'

# 查询回测结果
curl "http://localhost:8000/api/backtest/result/{task_id}"
```

#### 方法 3：通过 Python 脚本

```python
# examples/simple_backtest.py
import requests

# 配置回测参数
backtest_config = {
    "strategy": "double_ma",
    "symbol": "000001.SZ",
    "start_date": "2023-01-01",
    "end_date": "2023-12-31",
    "initial_cash": 100000,
    "params": {
        "fast_period": 5,
        "slow_period": 20
    }
}

# 调用回测 API
response = requests.post(
    "http://localhost:8000/api/backtest/run",
    json=backtest_config
)
result = response.json()

# 打印结果
print(f"年化收益率: {result['annual_return']:.2%}")
print(f"最大回撤: {result['max_drawdown']:.2%}")
print(f"夏普比率: {result['sharpe_ratio']:.2f}")
```

### 理解关键指标

回测报告包含以下关键指标：

| 指标 | 说明 | 理想值 |
|------|------|--------|
| **年化收益率** | 年化后的收益率 | > 10% |
| **最大回撤** | 最大亏损幅度 | < 20% |
| **夏普比率** | 风险调整后收益 | > 1.0 |
| **胜率** | 盈利交易占比 | > 50% |
| **盈亏比** | 平均盈利/平均亏损 | > 1.5 |
| **交易次数** | 总交易次数 | 适中（避免过度交易） |

**⚠️ 提醒**：历史表现不代表未来收益！

---

## 🔧 常见启动问题 FAQ

### 1. Docker 启动失败

**问题**：`docker compose up` 报错

**解决方案**：
```bash
# 检查 Docker 是否正常运行
docker info

# 检查端口是否被占用
lsof -i :8501  # Web UI 端口
lsof -i :8000  # API 端口

# 重新构建镜像
docker compose build --no-cache
docker compose up -d
```

### 2. 数据获取失败

**问题**：`Tushare API error` 或 `数据为空`

**解决方案**：
```bash
# 检查 Tushare Token 是否正确
cat .env | grep TUSHARE_TOKEN

# 测试 Tushare API
python3 -c "
import tushare as ts
ts.set_token('your_token_here')
pro = ts.pro_api()
print(pro.trade_cal(exchange='SSE', start_date='20230101', end_date='20230110'))
"

# 检查网络连接
ping tushare.pro
```

### 3. 端口冲突

**问题**：`Port 8501 is already in use`

**解决方案**：
```bash
# 方法 1：修改 docker-compose.yml 中的端口映射
# 将 "8501:8501" 改为 "8502:8501"

# 方法 2：停止占用端口的服务
lsof -ti:8501 | xargs kill -9

# 方法 3：使用不同端口启动
PORT_WEB=8502 PORT_API=8001 docker compose up -d
```

### 4. 镜像构建失败

**问题**：`ERROR: failed to solve: process "/bin/sh -c pip install"` 失败

**解决方案**：
```bash
# 使用国内镜像源
docker compose build --build-arg PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple

# 或在 Dockerfile 中添加
# RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### 5. 数据库连接失败

**问题**：`could not connect to server: Connection refused`

**解决方案**：
```bash
# 检查 PostgreSQL 容器状态
docker compose ps postgres

# 查看日志
docker compose logs postgres

# 重启数据库服务
docker compose restart postgres

# 等待 10 秒后检查
docker compose exec postgres pg_isready
```

### 6. 内存不足

**问题**：`OOMKilled` 或容器频繁重启

**解决方案**：
```bash
# 增加 Docker 内存限制（Docker Desktop 设置）
# Settings -> Resources -> Memory: 至少 4GB

# 或在 docker-compose.yml 中限制内存
services:
  web:
    deploy:
      resources:
        limits:
          memory: 2G
```

---

## 📖 下一步学习路径

### 1. 编写自己的策略

📖 [策略开发指南](docs/STRATEGY_DEVELOPMENT.md)（TODO）

**学习内容**：
- 策略模板结构
- 如何使用指标和因子
- 信号生成逻辑
- 仓位管理
- 风控规则

### 2. 详细功能使用

📖 [用户手册](docs/USER_GUIDE.md)

**学习内容**：
- Web UI 详细使用
- LLM Agent 交互技巧
- 数据管理功能
- 回测结果深度分析
- 实盘操作流程

### 3. 理解系统架构

📖 [架构设计](docs/ARCHITECTURE.md)

**学习内容**：
- 系统整体架构
- 核心模块设计
- 数据流和交易流
- 技术选型理由
- 性能优化策略

### 4. 产品功能规划

📖 [产品需求文档](docs/PRD.md)

**学习内容**：
- 目标用户画像
- 核心功能需求
- 产品路线图
- 成功指标

### 5. 参与项目开发

📖 [贡献指南](CONTRIBUTING.md)（TODO）

**学习内容**：
- 如何提交 Issue
- 如何提交 Pull Request
- 代码规范
- 测试要求

---

## 🛠️ 常用操作命令

### 服务管理

```bash
# 启动服务
docker compose up -d

# 停止服务
docker compose down

# 重启服务
docker compose restart

# 查看日志
docker compose logs -f [service_name]

# 进入容器
docker compose exec web bash
docker compose exec api bash

# 清理所有数据（危险操作！）
docker compose down -v
```

### 数据管理

```bash
# 更新数据
docker compose exec api python scripts/update_data.py

# 导出数据
docker compose exec api python scripts/export_data.py --symbol 000001.SZ

# 数据质量检查
docker compose exec api python scripts/check_data.py
```

### 备份与恢复

```bash
# 备份数据库
docker compose exec postgres pg_dump -U taurus taurus_aquant > backup_$(date +%Y%m%d).sql

# 恢复数据库
cat backup_20260302.sql | docker compose exec -T postgres psql -U taurus taurus_aquant
```

---

## 🆘 获取帮助

- **文档**：[完整文档目录](../README.md#-文档导航)
- **FAQ**：[常见问题](docs/FAQ.md)（TODO）
- **Issues**：[提交问题](https://github.com/yourusername/taurus-Aquant/issues)
- **讨论区**：[GitHub Discussions](https://github.com/yourusername/taurus-Aquant/discussions)

---

## ⚠️ 重要提醒

1. **风险提示**：使用本系统进行实盘交易可能导致资金损失，请务必阅读 [风险免责声明](RISK_DISCLAIMER.md)
2. **数据安全**：不要将 `.env` 文件提交到 Git 仓库
3. **合规要求**：使用本系统需遵守所在地的法律法规
4. **学习为主**：建议先在仿真环境充分测试，再考虑小额实盘

---

**🎉 恭喜！您已完成快速入门。开始探索 Taurus-AQuant 的强大功能吧！**
