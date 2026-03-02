# 安装部署文档

**Taurus-AQuant 详细安装与配置指南**

---

## 📋 目录

- [安装方式对比](#安装方式对比)
- [Docker 部署（推荐）](#docker-部署推荐)
- [本地开发环境](#本地开发环境)
- [数据库配置](#数据库配置)
- [API Key 配置](#api-key-配置)
- [环境变量说明](#环境变量说明)
- [可选组件安装](#可选组件安装)
- [常见安装问题 FAQ](#常见安装问题-faq)

---

## 安装方式对比

| 方式 | 难度 | 性能 | 适用场景 | 推荐度 |
|------|------|------|----------|--------|
| **Docker 部署** | ⭐ | ⭐⭐⭐⭐ | 生产环境、新手用户 | ⭐⭐⭐⭐⭐ |
| **本地开发环境** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 开发者、调试代码 | ⭐⭐⭐⭐ |
| **云服务器部署** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 7x24 小时运行 | ⭐⭐⭐⭐ |

**推荐**：新手用户优先使用 Docker 部署，简单快速。

---

## Docker 部署（推荐）

### 前置条件

- **Docker Desktop** 20.10+
  - [Windows 下载](https://www.docker.com/products/docker-desktop)
  - [macOS 下载](https://www.docker.com/products/docker-desktop)
  - [Linux 安装](https://docs.docker.com/engine/install/)

- **系统资源**
  - 内存：至少 4GB RAM（推荐 8GB+）
  - 磁盘：至少 10GB 可用空间
  - CPU：双核及以上

### 步骤 1：克隆项目

```bash
# 使用 Git 克隆
git clone https://github.com/yourusername/taurus-Aquant.git
cd taurus-Aquant

# 或者下载 ZIP 压缩包
wget https://github.com/yourusername/taurus-Aquant/archive/refs/heads/main.zip
unzip main.zip
cd taurus-Aquant-main
```

### 步骤 2：配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件
nano .env  # 或使用你喜欢的编辑器
```

**最小配置（必需）**：

```bash
# Tushare Token（必需）
TUSHARE_TOKEN=your_tushare_token_here
```

**完整配置示例**：

```bash
# Tushare 数据源配置
TUSHARE_TOKEN=your_tushare_token_here

# OpenAI API 配置（可选，用于 LLM Agent）
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4

# 数据库配置
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=taurus_aquant
POSTGRES_USER=taurus
POSTGRES_PASSWORD=taurus123

# Redis 配置
REDIS_HOST=redis
REDIS_PORT=6379

# 服务端口配置
PORT_WEB=8501
PORT_API=8000

# 日志级别
LOG_LEVEL=INFO
```

### 步骤 3：构建并启动服务

```bash
# 构建镜像（首次启动或代码更新后需要）
docker compose build

# 启动所有服务（后台运行）
docker compose up -d

# 查看服务状态
docker compose ps

# 查看日志
docker compose logs -f

# 查看特定服务日志
docker compose logs -f web
docker compose logs -f api
```

### 步骤 4：验证服务

```bash
# 检查服务健康状态
docker compose ps

# 预期输出：
# NAME                STATUS              PORTS
# taurus-web          Up (healthy)        0.0.0.0:8501->8501/tcp
# taurus-api          Up (healthy)        0.0.0.0:8000->8000/tcp
# taurus-postgres     Up (healthy)        5432/tcp
# taurus-redis        Up (healthy)        6379/tcp

# 测试 API 连接
curl http://localhost:8000/health

# 预期输出：
# {"status": "healthy", "database": "ok", "redis": "ok"}
```

### 步骤 5：访问服务

- **Web UI**: http://localhost:8501
- **API 文档**: http://localhost:8000/docs
- **API Redoc**: http://localhost:8000/redoc

### 数据持久化

Docker 容器的数据存储在 Docker Volume 中，即使删除容器也不会丢失：

```bash
# 查看数据卷
docker volume ls

# 备份数据卷
docker run --rm -v taurus-aquant_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz /data

# 恢复数据卷
docker run --rm -v taurus-aquant_postgres_data:/data -v $(pwd):/backup alpine tar xzf /backup/postgres_backup.tar.gz -C /
```

### 常用操作命令

```bash
# 停止服务
docker compose down

# 重启服务
docker compose restart

# 停止并删除容器（保留数据）
docker compose down

# 停止并删除容器和数据（危险操作！）
docker compose down -v

# 进入容器
docker compose exec web bash
docker compose exec api bash
docker compose exec postgres bash

# 查看日志
docker compose logs -f

# 重新构建镜像
docker compose build --no-cache
docker compose up -d
```

---

## 本地开发环境

### 前置条件

- **Python** 3.10+
- **PostgreSQL** 15+
- **Redis** 7+
- **Git**

### 步骤 1：克隆项目

```bash
git clone https://github.com/yourusername/taurus-Aquant.git
cd taurus-Aquant
```

### 步骤 2：创建虚拟环境

```bash
# 使用 venv
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows

# 或使用 conda
conda create -n taurus python=3.10
conda activate taurus
```

### 步骤 3：安装依赖

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装开发依赖（可选）
pip install -r requirements-dev.txt
```

### 步骤 4：安装数据库

#### macOS (Homebrew)

```bash
# 安装 PostgreSQL
brew install postgresql@15
brew services start postgresql@15

# 安装 Redis
brew install redis
brew services start redis
```

#### Ubuntu/Debian

```bash
# 安装 PostgreSQL
sudo apt update
sudo apt install postgresql-15 postgresql-contrib-15
sudo systemctl start postgresql

# 安装 Redis
sudo apt install redis-server
sudo systemctl start redis
```

#### Windows

1. 下载并安装 [PostgreSQL](https://www.postgresql.org/download/windows/)
2. 下载并安装 [Redis](https://github.com/microsoftarchive/redis/releases)

### 步骤 5：配置数据库

```bash
# 创建数据库
createdb taurus_aquant

# 或使用 psql
psql postgres
CREATE DATABASE taurus_aquant;
CREATE USER taurus WITH PASSWORD 'taurus123';
GRANT ALL PRIVILEGES ON DATABASE taurus_aquant TO taurus;
\q

# 初始化数据库表
python scripts/init_db.py
```

### 步骤 6：配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件
nano .env
```

**本地开发配置**：

```bash
# 数据源配置
TUSHARE_TOKEN=your_tushare_token_here

# OpenAI API（可选）
OPENAI_API_KEY=sk-your-openai-api-key-here

# 数据库配置（本地）
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=taurus_aquant
POSTGRES_USER=taurus
POSTGRES_PASSWORD=taurus123

# Redis 配置（本地）
REDIS_HOST=localhost
REDIS_PORT=6379
```

### 步骤 7：启动服务

```bash
# 启动 API 服务
cd src/api
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 新终端窗口：启动 Web UI
cd src/ui
streamlit run app.py --server.port 8501
```

### 步骤 8：验证服务

访问以下地址验证服务是否正常运行：

- **API 文档**: http://localhost:8000/docs
- **Web UI**: http://localhost:8501

---

## 数据库配置

### PostgreSQL 配置

#### 连接参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `POSTGRES_HOST` | `postgres` (Docker) / `localhost` (本地) | 数据库主机 |
| `POSTGRES_PORT` | `5432` | 数据库端口 |
| `POSTGRES_DB` | `taurus_aquant` | 数据库名称 |
| `POSTGRES_USER` | `taurus` | 用户名 |
| `POSTGRES_PASSWORD` | `taurus123` | 密码 |

#### 性能优化

编辑 `postgresql.conf`：

```ini
# 内存配置
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 16MB

# 连接配置
max_connections = 100

# 日志配置
logging_collector = on
log_directory = 'pg_log'
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
```

#### 备份与恢复

```bash
# 备份数据库
pg_dump -U taurus taurus_aquant > backup_$(date +%Y%m%d).sql

# 恢复数据库
psql -U taurus taurus_aquant < backup_20260302.sql
```

### Redis 配置

#### 连接参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `REDIS_HOST` | `redis` (Docker) / `localhost` (本地) | Redis 主机 |
| `REDIS_PORT` | `6379` | Redis 端口 |
| `REDIS_PASSWORD` | （空） | Redis 密码（可选） |

#### 性能优化

编辑 `redis.conf`：

```ini
# 内存配置
maxmemory 2gb
maxmemory-policy allkeys-lru

# 持久化配置
save 900 1
save 300 10
save 60 10000

# 日志配置
loglevel notice
```

---

## API Key 配置

### Tushare Token（必需）

Tushare 是免费的数据源，但需要注册获取 Token。

1. 访问 [Tushare 官网](https://tushare.pro/register)
2. 注册账号并登录
3. 在"个人中心"获取 Token
4. 将 Token 填入 `.env` 文件：

```bash
TUSHARE_TOKEN=your_tushare_token_here
```

**注意**：
- 免费版有调用频率限制（每分钟 200 次）
- 部分高级数据需要积分权限
- 积分可通过签到、分享等方式获取

### OpenAI API Key（可选）

用于 LLM Agent 功能。

1. 访问 [OpenAI 官网](https://platform.openai.com/)
2. 注册账号并登录
3. 在"API Keys"页面创建新的 API Key
4. 将 API Key 填入 `.env` 文件：

```bash
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4  # 或 gpt-3.5-turbo
```

**注意**：
- OpenAI API 是付费服务，需要充值
- 建议设置使用限额，避免超支
- 可以使用 gpt-3.5-turbo 降低成本

### 券商接口配置（可选）

用于实盘交易功能。

#### XTP 接口（中泰证券）

1. 在中泰证券开户并申请量化交易权限
2. 获取账户信息和密钥
3. 将配置填入 `.env` 文件：

```bash
XTP_ACCOUNT=your_account_here
XTP_PASSWORD=your_password_here
XTP_SERVER_IP=120.27.164.138
XTP_SERVER_PORT=6001
```

**注意**：
- 实盘交易有风险，请谨慎操作
- 建议先在仿真环境测试

---

## 环境变量说明

### 完整环境变量表

| 变量名 | 必需 | 默认值 | 说明 |
|--------|------|--------|------|
| **数据源配置** |
| `TUSHARE_TOKEN` | ✅ | - | Tushare Pro Token |
| **LLM 配置** |
| `OPENAI_API_KEY` | ❌ | - | OpenAI API Key |
| `OPENAI_MODEL` | ❌ | `gpt-4` | OpenAI 模型名称 |
| `OLLAMA_HOST` | ❌ | `http://localhost:11434` | Ollama 服务地址 |
| `OLLAMA_MODEL` | ❌ | `llama2` | Ollama 模型名称 |
| **数据库配置** |
| `POSTGRES_HOST` | ✅ | `postgres` | PostgreSQL 主机 |
| `POSTGRES_PORT` | ✅ | `5432` | PostgreSQL 端口 |
| `POSTGRES_DB` | ✅ | `taurus_aquant` | 数据库名称 |
| `POSTGRES_USER` | ✅ | `taurus` | 用户名 |
| `POSTGRES_PASSWORD` | ✅ | `taurus123` | 密码 |
| **缓存配置** |
| `REDIS_HOST` | ✅ | `redis` | Redis 主机 |
| `REDIS_PORT` | ✅ | `6379` | Redis 端口 |
| `REDIS_PASSWORD` | ❌ | - | Redis 密码 |
| **服务配置** |
| `PORT_WEB` | ❌ | `8501` | Web UI 端口 |
| `PORT_API` | ❌ | `8000` | API 服务端口 |
| `LOG_LEVEL` | ❌ | `INFO` | 日志级别（DEBUG/INFO/WARNING/ERROR） |
| **券商配置** |
| `XTP_ACCOUNT` | ❌ | - | XTP 账号 |
| `XTP_PASSWORD` | ❌ | - | XTP 密码 |
| `XTP_SERVER_IP` | ❌ | - | XTP 服务器 IP |
| `XTP_SERVER_PORT` | ❌ | - | XTP 服务器端口 |

### 环境变量优先级

1. 系统环境变量
2. `.env` 文件
3. 默认值

---

## 可选组件安装

### Qlib（微软量化平台）

Qlib 是微软开源的量化投资平台，提供丰富的因子库和模型。

```bash
# 安装 Qlib
pip install pyqlib

# 初始化 Qlib
python -m qlib.run.init

# 下载预训练模型
python scripts/download_qlib_data.py
```

**配置 `.env`**：

```bash
ENABLE_QLIB=true
QLIB_DATA_PATH=/path/to/qlib/data
```

### Ollama（本地 LLM）

Ollama 可以在本地运行大语言模型，无需调用 OpenAI API。

1. 下载并安装 [Ollama](https://ollama.ai/)
2. 拉取模型：

```bash
# 拉取 Llama2 模型
ollama pull llama2

# 拉取其他模型
ollama pull mistral
ollama pull codellama
```

3. 启动 Ollama 服务：

```bash
ollama serve
```

4. 配置 `.env`：

```bash
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama2
```

---

## 常见安装问题 FAQ

### 1. Docker 启动失败

**问题**：`docker compose up` 报错

**解决方案**：

```bash
# 检查 Docker 是否正常运行
docker info

# 检查端口是否被占用
lsof -i :8501
lsof -i :8000

# 杀掉占用端口的进程
kill -9 <PID>

# 重新构建镜像
docker compose build --no-cache
docker compose up -d
```

### 2. 数据库连接失败

**问题**：`could not connect to server: Connection refused`

**解决方案**：

```bash
# 检查 PostgreSQL 容器状态
docker compose ps postgres

# 查看 PostgreSQL 日志
docker compose logs postgres

# 重启 PostgreSQL 服务
docker compose restart postgres

# 进入 PostgreSQL 容器检查
docker compose exec postgres psql -U taurus -d taurus_aquant
```

### 3. Redis 连接失败

**问题**：`Redis connection refused`

**解决方案**：

```bash
# 检查 Redis 容器状态
docker compose ps redis

# 查看 Redis 日志
docker compose logs redis

# 测试 Redis 连接
docker compose exec redis redis-cli ping

# 预期输出：PONG
```

### 4. 镜像构建失败

**问题**：`ERROR: failed to solve: process "/bin/sh -c pip install"`

**解决方案**：

```bash
# 使用国内镜像源
docker compose build --build-arg PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple

# 或在 Dockerfile 中添加
# RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### 5. Python 依赖安装失败

**问题**：`ERROR: Could not find a version that satisfies the requirement`

**解决方案**：

```bash
# 升级 pip
pip install --upgrade pip

# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或配置 pip 镜像源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
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

### 7. 权限问题

**问题**：`Permission denied`

**解决方案**：

```bash
# 给脚本执行权限
chmod +x scripts/*.py

# 或使用 sudo（不推荐）
sudo docker compose up -d
```

### 8. 数据获取失败

**问题**：`Tushare API error`

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

### 9. API 启动失败

**问题**：`ModuleNotFoundError: No module named 'xxx'`

**解决方案**：

```bash
# 确保虚拟环境已激活
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows

# 重新安装依赖
pip install -r requirements.txt

# 检查 Python 版本
python --version  # 应该是 3.10+
```

### 10. Web UI 无法访问

**问题**：浏览器无法打开 http://localhost:8501

**解决方案**：

```bash
# 检查服务是否运行
docker compose ps web

# 查看 Web UI 日志
docker compose logs web

# 检查防火墙设置
# macOS: System Preferences -> Security & Privacy -> Firewall
# Windows: Control Panel -> System and Security -> Windows Firewall

# 尝试使用 127.0.0.1 而不是 localhost
http://127.0.0.1:8501
```

---

## 下一步

- 📖 [快速入门指南](QUICKSTART.md)
- 📚 [用户手册](USER_GUIDE.md)
- 🏗️ [架构设计](ARCHITECTURE.md)

---

## 获取帮助

- **GitHub Issues**: [提交问题](https://github.com/yourusername/taurus-Aquant/issues)
- **文档**: [完整文档目录](../README.md#-文档导航)
- **邮件**: your.email@example.com

---

**最后更新时间**：2026-03-02
