# Taurus-AQuant

<!-- 顶部徽章 -->
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Documentation](https://img.shields.io/badge/Docs-Latest-green.svg)](docs/)
[![Status](https://img.shields.io/badge/Status-Developing-orange.svg)]()

**一个面向个人投资者的 A股/ETF 算法交易项目：集成回测、数据、实盘网关与大模型 Agent**

[English](README_EN.md) | 简体中文

---

## ⚠️ 风险提示

**本项目涉及真实资金交易，可能导致本金损失。使用前请务必阅读 [风险免责声明](docs/RISK_DISCLAIMER.md)。**

---

## 项目简介

Taurus-AQuant 是一个面向个人投资者的"傻瓜式" A股/ETF 算法交易项目模板，支持容器化部署与本地一键启动，帮助您从 0 到 1 快速搭建可交互的量化交易系统。

### 核心价值主张

- **🚀 零门槛启动**：Docker 一键部署，15 分钟完成第一个回测
- **🤖 AI 驱动**：集成大语言模型（LLM），支持自然语言生成策略
- **📊 专业回测**：内置 Backtrader/Rqalpha 双引擎，支持完整的中国市场特性
- **🔗 实盘预备**：预留 vn.py 网关，支持仿真交易和小额实盘灰度
- **🔧 高度可扩展**：模块化设计，支持自定义策略、因子、风控规则

### 目标人群

- **量化新手**：想学习算法交易但不知从何入手
- **个人投资者**：希望用技术手段提升投资效率
- **AI 爱好者**：探索大语言模型在金融领域的应用
- **开发者**：需要一个完整的量化交易项目模板

---

## 📚 快速导航

| 文档 | 描述 | 适用人群 |
|------|------|----------|
| [🚀 快速入门](docs/QUICKSTART.md) | 15 分钟快速体验 | 新手必读 |
| [📖 用户手册](docs/USER_GUIDE.md) | 详细功能使用说明 | 所有用户 |
| [🏗️ 架构设计](docs/ARCHITECTURE.md) | 系统架构与技术细节 | 开发者 |
| [📋 产品需求](docs/PRD.md) | 功能规划与需求定义 | 产品经理 |
| [🗺️ 发展路线](docs/ROADMAP.md) | 项目发展方向 | 所有用户 |
| [⚙️ 安装部署](docs/INSTALLATION.md) | 详细部署文档 | 运维人员 |

---

## 核心特性

### ✨ 一键启动
- `docker compose up` 即可启动 Web UI、API 服务、回测服务与 Agent 服务
- 完整的容器化部署，无需复杂环境配置
- 支持本地开发模式和云端部署

### 📊 回测与研究
- 内置 Backtrader 与 Rqalpha 两套回测管线（二选一或并行）
- 严格的中国交易日历、停牌/复权与费用模型参数位
- 完整的绩效分析报告（夏普比率、最大回撤、年化收益等）
- 支持多周期、多品种、多策略组合回测

### 📈 数据接入
- AkShare/Tushare 适配；提供数据落地与快照缓存
- 支持日线、分钟线、Tick 级数据
- 自动处理停牌、复权、分红等公司行为
- 数据质量检查和缺失值处理

### 🔌 实盘预备
- 预留 vn.py 网关接入位（XTP/OpenAPI）
- 先跑仿真/纸交易，再灰度实盘
- 完整的风控系统（仓位、频率、黑名单等）
- 支持多账户管理

### 🤖 LLM Agent 交互
- 策略问答、回测指令生成、风控检查清单
- 自然语言生成策略代码（Python）
- 交易计划 JSON 输出与校验
- 支持多种大模型（OpenAI GPT、Claude、本地 LLM）

### 🔧 可插拔组件
- 执行器（限价/TWAP/VWAP）
- 风控（仓位/回撤/涨跌停）
- 指标与因子库
- 数据源适配器

---

## 🛠️ 技术栈

| 类别 | 技术选型 | 说明 |
|------|----------|------|
| **编程语言** | Python 3.10+ | 主要开发语言 |
| **Web 框架** | FastAPI | 高性能异步 API 框架 |
| **前端 UI** | Streamlit / Gradio | 快速构建交互式界面 |
| **回测引擎** | Backtrader / Rqalpha | 成熟的量化回测框架 |
| **实盘网关** | vn.py | 开源量化交易框架 |
| **数据源** | AkShare / Tushare | 免费 A股数据源 |
| **LLM 集成** | OpenAI API / Ollama | 大语言模型接口 |
| **数据库** | PostgreSQL | 关系型数据库 |
| **缓存** | Redis | 高性能缓存 |
| **容器化** | Docker / Docker Compose | 应用容器化部署 |
| **可选组件** | Qlib | 微软量化投资平台 |

---

## 🚀 快速开始

### 前置条件

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)（推荐）
- Python 3.10+（可选，用于本地开发）
- API Key（Tushare / OpenAI）

### 3 步启动

```bash
# 1. 克隆项目
git clone https://github.com/yourusername/taurus-Aquant.git
cd taurus-Aquant

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入您的 API Key

# 3. 启动服务
docker compose up
```

### 访问服务

- **Web UI**: http://localhost:8501 (Streamlit)
- **API 文档**: http://localhost:8000/docs (FastAPI Swagger)
- **回测报告**: http://localhost:8501/reports

### 第一个回测示例

详细步骤请参考 [快速入门指南](docs/QUICKSTART.md)。

---

## 📖 文档导航

### 基础文档
- [风险免责声明](docs/RISK_DISCLAIMER.md) - **必读**
- [快速入门](docs/QUICKSTART.md) - 15 分钟快速体验
- [安装部署](docs/INSTALLATION.md) - 详细部署文档

### 产品规划
- [产品需求文档](docs/PRD.md) - 功能定义与需求规格
- [发展路线图](docs/ROADMAP.md) - 版本规划与里程碑

### 技术文档
- [架构设计](docs/ARCHITECTURE.md) - 系统架构与模块设计
- [用户手册](docs/USER_GUIDE.md) - 详细使用说明

### 开发文档（TODO）
- [贡献指南](CONTRIBUTING.md) - 如何参与项目开发
- [开发文档](docs/DEVELOPMENT.md) - 本地开发环境搭建
- [API 文档](docs/API.md) - API 接口文档

---

## 📁 项目结构

```
taurus-Aquant/
├── README.md                   # 项目主页
├── LICENSE                     # 开源协议
├── .env.example                # 环境变量模板
├── docker-compose.yml          # Docker 编排文件
├── docs/                       # 文档目录
│   ├── RISK_DISCLAIMER.md      # 风险免责声明
│   ├── QUICKSTART.md           # 快速入门
│   ├── ROADMAP.md              # 路线图
│   ├── PRD.md                  # 产品需求文档
│   ├── ARCHITECTURE.md         # 架构设计
│   ├── INSTALLATION.md         # 安装部署
│   └── USER_GUIDE.md           # 用户手册
├── src/                        # 源代码目录
│   ├── api/                    # FastAPI 服务
│   ├── backtest/               # 回测引擎
│   ├── data/                   # 数据服务
│   ├── agent/                  # LLM Agent
│   ├── trading/                # 交易网关
│   ├── risk/                   # 风控系统
│   └── ui/                     # Web UI
├── tests/                      # 测试代码
├── configs/                    # 配置文件
├── scripts/                    # 工具脚本
└── requirements.txt            # Python 依赖
```

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 贡献方式

- **报告 Bug**：通过 [GitHub Issues](https://github.com/yourusername/taurus-Aquant/issues) 提交 Bug 报告
- **功能建议**：提出新功能想法或改进建议
- **代码贡献**：提交 Pull Request 修复 Bug 或添加功能
- **文档改进**：完善文档、修正错误、添加示例
- **策略分享**：分享您的交易策略和回测结果

### 贡献者招募

我们需要以下方面的贡献者：
- **策略开发者**：分享有效的交易策略
- **数据工程师**：优化数据获取和存储
- **前端开发者**：改进 Web UI 体验
- **测试工程师**：编写测试用例，提升代码质量

详细贡献指南请参考 [CONTRIBUTING.md](CONTRIBUTING.md)（TODO）。

---

## 📜 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

---

## ⚖️ 法律声明

- 本项目 **仅供学习和研究使用**
- **不构成任何投资建议**
- 使用本项目进行实盘交易 **可能产生资金损失**
- 用户需 **自行承担所有风险**
- 请确保遵守所在地的 **法律法规**

详见 [风险免责声明](docs/RISK_DISCLAIMER.md)。

---

## 📞 联系方式

- **GitHub**: [https://github.com/yourusername/taurus-Aquant](https://github.com/yourusername/taurus-Aquant)
- **Issues**: [提交问题](https://github.com/yourusername/taurus-Aquant/issues)
- **Email**: your.email@example.com

---

## 🙏 致谢

感谢以下开源项目的支持：

- [Backtrader](https://www.backtrader.com/)
- [Rqalpha](https://github.com/ricequant/rqalpha)
- [vn.py](https://www.vnpy.com/)
- [AkShare](https://github.com/akfamily/akshare)
- [Tushare](https://tushare.pro/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)

---

## ⭐ Star History

如果这个项目对您有帮助，请给我们一个 ⭐ Star！

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/taurus-Aquant&type=Date)](https://star-history.com/#yourusername/taurus-Aquant&Date)

---

**投资有风险，入市需谨慎！**
