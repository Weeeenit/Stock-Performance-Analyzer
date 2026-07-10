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
# Safety Check
# =====================================================

if len(df) < 30:
    st.warning("Not enough data for risk analysis.")
    st.stop()

# =====================================================
# Calculations
# =====================================================

try:

    volatility = calculate_volatility(df)
    sharpe = calculate_sharpe_ratio(df)
    var95 = calculate_var(df)

    df = calculate_drawdown(df)
    df = rolling_volatility(df)

except Exception as e:

    st.error(f"Calculation Error: {e}")
    st.stop()

returns = df["Close"].pct_change().dropna() * 100

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
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    width="stretch"
)

st.divider()

# =====================================================
# Drawdown
# =====================================================

st.subheader("Drawdown")

fig = px.line(
    df,
    x="Date",
    y="Drawdown"
)

fig.update_layout(
    template="plotly_dark",
    height=450,
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    width="stretch"
)

st.divider()

# =====================================================
# Return Distribution
# =====================================================

st.subheader("Daily Return Distribution")

hist_df = returns.to_frame(name="Daily Return")

fig = px.histogram(
    hist_df,
    x="Daily Return",
    nbins=60
)

fig.update_layout(
    template="plotly_dark",
    height=450
)

st.plotly_chart(
    fig,
    width="stretch"
)

st.divider()

# =====================================================
# Additional Statistics
# =====================================================

st.subheader("Additional Statistics")

left, right = st.columns(2)

with left:

    st.metric(
        "Average Daily Return",
        f"{returns.mean():.2f}%"
    )

    st.metric(
        "Best Daily Return",
        f"{returns.max():.2f}%"
    )

with right:

    st.metric(
        "Worst Daily Return",
        f"{returns.min():.2f}%"
    )

    st.metric(
        "Daily Return Std Dev",
        f"{returns.std():.2f}%"
    )

st.divider()

# =====================================================
# Interpretation
# =====================================================

st.subheader("Risk Interpretation")

if risk == "Low":

    st.success(
        "This stock has shown relatively low historical volatility."
    )

elif risk == "Medium":

    st.warning(
        "This stock has shown moderate historical volatility."
    )

else:

    st.error(
        "This stock has shown high historical volatility."
    )