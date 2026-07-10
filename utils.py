from pathlib import Path
import pandas as pd
import numpy as np

# =====================================================
# DATA CONFIGURATION
# =====================================================

DATA_FOLDER = Path("Data/cleaned")


# =====================================================
# DATA LOADING
# =====================================================

def get_stock_list():
    """Return all available stock names."""
    return sorted([file.stem for file in DATA_FOLDER.glob("*.csv")])


def load_stock(stock_name):
    """Load stock data."""
    file_path = DATA_FOLDER / f"{stock_name}.csv"

    df = pd.read_csv(file_path)

    df["Date"] = pd.to_datetime(df["Date"])

    numeric_cols = ["Open", "High", "Low", "Close", "Volume"]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.sort_values("Date").reset_index(drop=True)

    return df


def filter_data(df, start_date, end_date):
    """Filter dataframe between dates."""

    return df[
        (df["Date"] >= pd.to_datetime(start_date))
        &
        (df["Date"] <= pd.to_datetime(end_date))
    ].copy()


# =====================================================
# OVERVIEW
# =====================================================

def calculate_kpis(df):

    return {
        "Current Price": df["Close"].iloc[-1],
        "Highest Price": df["High"].max(),
        "Lowest Price": df["Low"].min(),
        "Total Return": (
            (
                df["Close"].iloc[-1]
                -
                df["Close"].iloc[0]
            )
            /
            df["Close"].iloc[0]
        ) * 100
    }


def calculate_statistics(df):

    return {
        "Trading Days": len(df),
        "Average Close": df["Close"].mean(),
        "Average Volume": df["Volume"].mean(),
        "Highest Volume": df["Volume"].max(),
        "Highest Price": df["High"].max(),
        "Lowest Price": df["Low"].min()
    }


# =====================================================
# PRICE ANALYSIS
# =====================================================

def add_moving_averages(df):

    df = df.copy()

    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()
    df["MA200"] = df["Close"].rolling(200).mean()

    return df


def calculate_bollinger_bands(df):

    df = df.copy()

    df["MA20"] = df["Close"].rolling(20).mean()

    std = df["Close"].rolling(20).std()

    df["Upper Band"] = df["MA20"] + (2 * std)
    df["Lower Band"] = df["MA20"] - (2 * std)

    return df


def get_trend(df):

    df = add_moving_averages(df)

    latest = df.iloc[-1]

    if pd.isna(latest["MA200"]):
        return "Insufficient Data"

    if latest["Close"] > latest["MA200"]:
        return "Bullish"

    elif latest["Close"] < latest["MA200"]:
        return "Bearish"

    return "Sideways"


# =====================================================
# RETURN ANALYSIS
# =====================================================

def calculate_daily_returns(df):

    df = df.copy()

    df["Daily Return"] = df["Close"].pct_change() * 100

    return df


def calculate_cumulative_returns(df):

    df = df.copy()

    returns = df["Close"].pct_change()

    df["Cumulative Return"] = (
        (1 + returns).cumprod() - 1
    ) * 100

    return df


def calculate_monthly_returns(df):

    df = df.copy()

    df = df.set_index("Date")

    monthly = df["Close"].resample("ME").last()

    monthly_returns = monthly.pct_change() * 100

    monthly_df = monthly_returns.reset_index()

    monthly_df.columns = ["Date", "Return"]

    monthly_df["Year"] = monthly_df["Date"].dt.year
    monthly_df["Month"] = monthly_df["Date"].dt.strftime("%b")

    heatmap = monthly_df.pivot(
        index="Year",
        columns="Month",
        values="Return"
    )

    month_order = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    heatmap = heatmap.reindex(columns=month_order)

    return heatmap


def calculate_yearly_returns(df):

    df = df.copy()

    df = df.set_index("Date")

    yearly = df["Close"].resample("YE").last()

    yearly_returns = yearly.pct_change() * 100

    yearly_returns.index = yearly_returns.index.year

    return yearly_returns

def get_return_statistics(df):

    return {

        "Average Return": df["Daily Return"].mean(),

        "Median Return": df["Daily Return"].median(),

        "Maximum Return": df["Daily Return"].max(),

        "Minimum Return": df["Daily Return"].min(),

        "Volatility": df["Daily Return"].std()

    }


# =====================================================
# RISK ANALYSIS
# =====================================================

def calculate_volatility(df):

    returns = df["Close"].pct_change()

    return returns.std() * np.sqrt(252) * 100


def calculate_sharpe_ratio(df, risk_free_rate=0.06):

    returns = df["Close"].pct_change().dropna()

    annual_return = returns.mean() * 252

    annual_volatility = returns.std() * np.sqrt(252)

    if annual_volatility == 0:
        return 0

    return (annual_return - risk_free_rate) / annual_volatility


def calculate_var(df, confidence=0.95):

    returns = df["Close"].pct_change().dropna()

    return np.percentile(
        returns,
        (1 - confidence) * 100
    ) * 100


def calculate_drawdown(df):

    df = df.copy()

    rolling_max = df["Close"].cummax()

    df["Drawdown"] = (
        (df["Close"] - rolling_max)
        /
        rolling_max
    ) * 100

    return df


def rolling_volatility(df, window=30):

    df = df.copy()

    returns = df["Close"].pct_change()

    df["Rolling Volatility"] = (
        returns
        .rolling(window)
        .std()
        * np.sqrt(252)
        * 100
    )

    return df


def risk_level(volatility):

    if volatility < 20:
        return "Low"

    elif volatility < 35:
        return "Medium"

    return "High"


# =====================================================
# INVESTMENT SIMULATOR
# =====================================================

def investment_simulator(df, investment):

    initial_price = df["Close"].iloc[0]

    final_price = df["Close"].iloc[-1]

    shares = investment / initial_price

    current_value = shares * final_price

    profit = current_value - investment

    total_return = (
        profit / investment
    ) * 100

    years = (
        (df["Date"].iloc[-1] - df["Date"].iloc[0]).days
    ) / 365.25

    if years > 0:

        cagr = (
            (current_value / investment)
            ** (1 / years)
            - 1
        ) * 100

    else:

        cagr = 0

    return {

        "Current Value": current_value,

        "Profit": profit,

        "Return": total_return,

        "CAGR": cagr

    }


def investment_growth(df, investment):

    df = df.copy()

    initial_price = df["Close"].iloc[0]

    shares = investment / initial_price

    df["Portfolio Value"] = shares * df["Close"]

    return df