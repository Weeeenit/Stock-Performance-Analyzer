import streamlit as st

st.set_page_config(
    page_title="Stock Performance Analyzer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

overview = st.Page(
    "pages/1_Overview.py",
    title="Overview",
    icon="🏠",
)

price = st.Page(
    "pages/2_Price_analysis.py",
    title="Price Analysis",
    icon="📈",
)

returns = st.Page(
    "pages/3_Return_analysis.py",
    title="Return Analysis",
    icon="💹",
)

risk = st.Page(
    "pages/4_Risk_analysis.py",
    title="Risk Analysis",
    icon="⚠️",
)

investment = st.Page(
    "pages/5_Investment_simulator.py",
    title="Investment Simulator",
    icon="💰",
)

pg = st.navigation(
    [
        overview,
        price,
        returns,
        risk,
        investment,
    ]
)

pg.run()