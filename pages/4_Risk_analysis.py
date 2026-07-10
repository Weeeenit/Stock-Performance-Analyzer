import streamlit as st
import plotly.express as px

from utils import (
    get_stock_list,
    load_stock,
    filter_data,
    calculate_volatility,
    calculate_sharpe_ratio,
    calculate_var,
    calculate_drawdown,
    rolling_volatility,
    risk_level
)

st.title("Risk Analysis")

# =====================================================
# Sidebar
# =====================================================

stocks = get_stock_list()

stock = st.sidebar.selectbox(
    "Select Stock",
    stocks,
    key="risk_stock"
)

df = load_stock(stock)

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    key="risk_date"
)

if len(date_range) == 2:

    start_date, end_date = date_range

    df = filter_data(df, start_date, end_date)

# =====================================================
# Calculations
# =====================================================

volatility = calculate_volatility(df)

sharpe = calculate_sharpe_ratio(df)

var95 = calculate_var(df)

df = calculate_drawdown(df)

df = rolling_volatility(df)

max_drawdown = df["Drawdown"].min()

risk = risk_level(volatility)

# =====================================================
# KPI Cards
# =====================================================

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Annualized Volatility",
    f"{volatility:.2f}%"
)

c2.metric(
    "Sharpe Ratio",
    f"{sharpe:.2f}"
)

c3.metric(
    "Maximum Drawdown",
    f"{max_drawdown:.2f}%"
)

c4.metric(
    "Value at Risk (95%)",
    f"{var95:.2f}%"
)

c5.metric(
    "Risk Level",
    risk
)

st.divider()

# =====================================================
# Rolling Volatility
# =====================================================

st.subheader("30-Day Rolling Volatility")

fig = px.line(
    df,
    x="Date",
    y="Rolling Volatility"
)

fig.update_layout(
    template="plotly_dark",
    height=450,
    hovermode="x unified",
    xaxis_title="Date",
    yaxis_title="Volatility (%)"
)

st.plotly_chart(
    fig,
    width="stretch"
)

st.divider()

# =====================================================
# Drawdown Chart
# =====================================================

st.subheader("Drawdown")

fig = px.area(
    df,
    x="Date",
    y="Drawdown"
)

fig.update_layout(
    template="plotly_dark",
    height=450,
    hovermode="x unified",
    xaxis_title="Date",
    yaxis_title="Drawdown (%)"
)

st.plotly_chart(
    fig,
    width="stretch"
)

st.divider()

# =====================================================
# Return Distribution
# =====================================================

returns = df["Close"].pct_change() * 100

st.subheader("Return Distribution")

fig = px.histogram(
    returns,
    nbins=60
)

fig.update_layout(
    template="plotly_dark",
    height=450,
    xaxis_title="Daily Return (%)",
    yaxis_title="Frequency"
)

st.plotly_chart(
    fig,
    width="stretch"
)

st.divider()

# =====================================================
# Risk Interpretation
# =====================================================

st.subheader("Risk Interpretation")

if risk == "Low":

    st.success(
        """
        This asset has relatively low historical volatility.
        Price movements have generally been stable over the selected period.
        """
    )

elif risk == "Medium":

    st.warning(
        """
        This asset exhibits moderate volatility.
        Investors should expect noticeable price fluctuations.
        """
    )

else:

    st.error(
        """
        This asset has experienced high historical volatility.
        Large price swings increase both potential returns and potential losses.
        """
    )

# =====================================================
# Additional Statistics
# =====================================================

st.subheader("Additional Risk Statistics")

left, right = st.columns(2)

with left:

    st.metric(
        "Average Daily Return",
        f"{returns.mean():.2f}%"
    )

    st.metric(
        "Maximum Daily Gain",
        f"{returns.max():.2f}%"
    )

with right:

    st.metric(
        "Worst Daily Loss",
        f"{returns.min():.2f}%"
    )

    st.metric(
        "Daily Return Std Dev",
        f"{returns.std():.2f}%"
    )