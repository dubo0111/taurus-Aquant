"""
Streamlit Web UI - 主应用
"""
import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objs as go
import plotly.express as px

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.data.data_service import DataService
from src.backtest.backtest_engine import BacktestEngine, BacktestConfig, generate_double_ma_signal
from src.utils.logger import logger
from src.utils.config import settings

# 页面配置
st.set_page_config(
    page_title=f"{settings.APP_NAME}",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义 CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .success {
        color: #28a745;
    }
    .warning {
        color: #ffc107;
    }
    .error {
        color: #dc3545;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_data_service():
    """获取数据服务实例（缓存）"""
    return DataService()


def main():
    """主函数"""
    # 标题
    st.markdown(f'<h1 class="main-header">📈 {settings.APP_NAME} v{settings.APP_VERSION}</h1>', unsafe_allow_html=True)
    st.markdown(f"**AI 驱动的 A股/ETF 算法交易平台** | [API 文档](http://localhost:{settings.API_PORT}/docs)")

    # 侧边栏
    st.sidebar.header("⚙️ 配置")

    # 数据源选择
    st.sidebar.subheader("数据源")
    data_service = get_data_service()
    st.sidebar.info(f"当前使用: **{data_service.adapter.__class__.__name__}**")

    # 主要功能
    page = st.sidebar.radio(
        "选择功能",
        ["🏠 首页", "📊 数据探索", "🔬 策略回测", "🤖 AI 助手", "⚙️ 系统设置"],
        index=0
    )

    if page == "🏠 首页":
        show_home_page()
    elif page == "📊 数据探索":
        show_data_exploration()
    elif page == "🔬 策略回测":
        show_backtest_page()
    elif page == "🤖 AI 助手":
        show_ai_assistant()
    elif page == "⚙️ 系统设置":
        show_settings()


def show_home_page():
    """显示首页"""
    st.header("🏠 系统概览")

    # 系统状态
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="数据源",
            value="Tushare",
            delta="在线"
        )

    with col2:
        st.metric(
            label="内置策略",
            value="3",
            delta="+2 开发中"
        )

    with col3:
        st.metric(
            label="回测引擎",
            value="Backtrader",
            delta="就绪"
        )

    # 快速开始
    st.subheader("🚀 快速开始")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 1️⃣ 数据探索
        浏览股票数据，查看历史行情
        """)
        if st.button("📊 开始探索", key="explore_btn"):
            st.info("请从左侧菜单选择 '📊 数据探索'")

    with col2:
        st.markdown("""
        ### 2️⃣ 策略回测
        测试交易策略的历史表现
        """)
        if st.button("🔬 开始回测", key="backtest_btn"):
            st.info("请从左侧菜单选择 '🔬 策略回测'")

    # 最近动态
    st.subheader("📈 最近动态")

    st.markdown("""
    **2026-03-02**
    - ✅ 完成 Tushare 数据源集成
    - ✅ 完成 AkShare 备用数据源
    - ✅ 完成基础回测引擎
    - 🔄 LLM Agent 集成中（智谱 AI）

    **下一步计划**
    - 📝 添加更多内置策略
    - 🎨 完善数据可视化
    - 🤖 集成 AI 助手
    """)


def show_data_exploration():
    """显示数据探索页面"""
    st.header("📊 数据探索")

    # 输入股票代码
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        symbol = st.text_input("股票代码", value="000001", help="例如: 000001 (平安银行)")

    with col2:
        days = st.selectbox("时间范围", [30, 60, 90, 180], index=0)

    with col3:
        if st.button("获取数据", type="primary"):
            st.session_state['fetch_data'] = True

    # 获取数据
    if st.session_state.get('fetch_data', False):
        try:
            with st.spinner("正在获取数据..."):
                data_service = get_data_service()

                end_date = datetime.now().strftime('%Y-%m-%d')
                start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

                # 获取数据
                df = data_service.get_daily_data(
                    symbol=symbol,
                    start_date=start_date,
                    end_date=end_date
                )

                if df.empty:
                    st.warning(f"未找到 {symbol} 的数据")
                    return

                st.session_state['stock_data'] = df
                st.success(f"✅ 成功获取 {len(df)} 条数据")

        except Exception as e:
            st.error(f"获取数据失败: {e}")
            logger.error(f"数据获取失败: {e}")

    # 显示数据
    if 'stock_data' in st.session_state:
        df = st.session_state['stock_data']

        # 数据统计
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("最新价格", f"{df.iloc[-1]['close']:.2f}")

        with col2:
            change_pct = (df.iloc[-1]['close'] / df.iloc[0]['close'] - 1) * 100
            st.metric("区间涨跌", f"{change_pct:.2f}%")

        with col3:
            st.metric("最高价", f"{df['high'].max():.2f}")

        with col4:
            st.metric("最低价", f"{df['low'].min():.2f}")

        # 价格走势图
        st.subheader("📈 价格走势")

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['close'],
            mode='lines',
            name='收盘价',
            line=dict(color='#1f77b4', width=2)
        ))

        fig.update_layout(
            title=f"{symbol} 价格走势",
            xaxis_title="日期",
            yaxis_title="价格",
            hovermode='x unified',
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

        # 数据表格
        st.subheader("📋 数据明细")
        st.dataframe(df.tail(20), use_container_width=True)


def show_backtest_page():
    """显示回测页面"""
    st.header("🔬 策略回测")

    # 回测配置
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("配置参数")

        symbol = st.text_input("股票代码", value="000001", key="backtest_symbol")

        start_date = st.date_input("开始日期", value=datetime(2024, 1, 1))
        end_date = st.date_input("结束日期", value=datetime(2024, 12, 31))

        initial_cash = st.number_input("初始资金", value=100000, min_value=10000, step=10000)

        strategy = st.selectbox("策略", ["双均线策略", "MACD 策略", "RSI 策略"])

        # 策略参数
        if strategy == "双均线策略":
            fast_period = st.slider("快线周期", 5, 30, 5)
            slow_period = st.slider("慢线周期", 10, 60, 20)

    with col2:
        st.subheader("策略说明")

        st.markdown(f"""
        **{strategy}**

        双均线策略是一种趋势跟踪策略：
        - **快线**: {fast_period} 日移动平均线
        - **慢线**: {slow_period} 日移动平均线

        **交易规则**:
        - 当快线上穿慢线时，买入
        - 当快线下穿慢线时，卖出

        **费用模型**:
        - 佣金: 0.03% (万三)
        - 印花税: 0.1% (千一，仅卖出)
        """)

    # 执行回测
    if st.button("🚀 开始回测", type="primary"):
        try:
            with st.spinner("回测执行中..."):
                data_service = get_data_service()

                # 获取数据
                df = data_service.get_daily_data(
                    symbol=symbol,
                    start_date=start_date.strftime('%Y-%m-%d'),
                    end_date=end_date.strftime('%Y-%m-%d')
                )

                if df.empty:
                    st.error("未找到数据")
                    return

                # 生成信号
                signals = generate_double_ma_signal(df, fast_period, slow_period)

                # 创建回测配置
                config = BacktestConfig(
                    symbol=symbol,
                    start_date=start_date.strftime('%Y-%m-%d'),
                    end_date=end_date.strftime('%Y-%m-%d'),
                    initial_cash=float(initial_cash)
                )

                # 执行回测
                engine = BacktestEngine(config)
                result = engine.run(df, signals)

                st.session_state['backtest_result'] = result
                st.success(f"✅ 回测完成！共 {result.total_trades} 笔交易")

        except Exception as e:
            st.error(f"回测失败: {e}")
            logger.error(f"回测失败: {e}", exc_info=True)

    # 显示结果
    if 'backtest_result' in st.session_state:
        result = st.session_state['backtest_result']

        # 绩效指标
        st.subheader("📊 绩效指标")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "总收益率",
                f"{result.total_return:.2%}",
                delta=f"{result.total_return:.2%}"
            )

        with col2:
            st.metric(
                "年化收益率",
                f"{result.annual_return:.2%}",
                delta=f"{result.annual_return:.2%}"
            )

        with col3:
            st.metric(
                "最大回撤",
                f"{result.max_drawdown:.2%}",
                delta_color="inverse"
            )

        with col4:
            st.metric(
                "夏普比率",
                f"{result.sharpe_ratio:.2f}"
            )

        col5, col6, col7, col8 = st.columns(4)

        with col5:
            st.metric("胜率", f"{result.win_rate:.2%}")

        with col6:
            st.metric("盈亏比", f"{result.profit_loss_ratio:.2f}")

        with col7:
            st.metric("总交易次数", f"{result.total_trades}")

        with col8:
            final_value = result.daily_values.iloc[-1]['total_value']
            st.metric("最终资产", f"{final_value:,.0f}")

        # 资产曲线
        st.subheader("📈 资产曲线")

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=result.daily_values['date'],
            y=result.daily_values['total_value'],
            mode='lines',
            name='资产价值',
            line=dict(color='#2ecc71', width=2)
        ))

        # 基准线（初始资金）
        fig.add_hline(
            y=config.initial_cash,
            line_dash="dash",
            line_color="gray",
            annotation_text="初始资金"
        )

        fig.update_layout(
            title="资产变化曲线",
            xaxis_title="日期",
            yaxis_title="资产价值",
            hovermode='x unified',
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

        # 交易记录
        if result.trades:
            st.subheader("📝 交易记录")

            trades_df = pd.DataFrame(result.trades)
            st.dataframe(trades_df, use_container_width=True)


def show_ai_assistant():
    """显示 AI 助手页面"""
    st.header("🤖 AI 助手")

    st.info("🚧 AI 助手功能开发中...")

    st.markdown("""
    ### 功能规划

    **AI 助手将提供以下功能**:

    1. **策略生成** 📝
       - 自然语言生成交易策略代码
       - 策略模板推荐

    2. **策略分析** 🔍
       - 识别策略风险点
       - 提供优化建议

    3. **市场解读** 📊
       - 解读市场新闻和事件
       - 分析市场趋势

    4. **交易计划** 📋
       - 生成每日交易计划
       - 风控检查清单

    ### 技术栈

    - 智谱 AI GLM-4
    - 本地 LLM (Ollama)
    - OpenAI GPT (可选)

    ### 当前状态

    ⚠️ **智谱 AI API 余额不足**

    请访问 https://open.bigmodel.cn/ 充值或激活免费额度后再使用 AI 功能。

    ---

    **临时替代方案**: 使用内置策略模板，无需 AI 即可进行回测。
    """)


def show_settings():
    """显示设置页面"""
    st.header("⚙️ 系统设置")

    st.subheader("系统信息")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        **应用配置**
        - 应用名称: {settings.APP_NAME}
        - 版本: {settings.APP_VERSION}
        - 调试模式: {'启用' if settings.DEBUG else '禁用'}
        - 日志级别: {settings.LOG_LEVEL}
        """)

    with col2:
        st.markdown(f"""
        **数据源配置**
        - Tushare Token: {'已配置 ✅' if settings.TUSHARE_TOKEN else '未配置 ❌'}
        - 智谱 AI Key: {'已配置 ✅' if settings.ZHIPU_API_KEY else '未配置 ❌'}
        - 数据缓存: {settings.DATA_CACHE_DIR}
        """)

    st.subheader("风控参数")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("最大仓位", f"{settings.RISK_MAX_POSITION_PCT:.0%}")

    with col2:
        st.metric("每日最大交易次数", f"{settings.RISK_MAX_DAILY_TRADES}")

    with col3:
        st.metric("止损线", f"{settings.RISK_STOP_LOSS_PCT:.0%}")

    st.info("⚠️ 风控参数可在 .env 文件中修改")


if __name__ == "__main__":
    main()
