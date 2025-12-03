import streamlit as st
import pandas as pd
from utils import load_data

st.set_page_config(
    page_title="Data Collection",
    page_icon="📑",
    layout="wide"
)
st.markdown("# Data Collection")
st.sidebar.header("Data Collection")
data = load_data()
col1, col2, col3 = st.columns(3)
    
with col1:
    st.metric("ML Task", "Binary Classification")
    st.info("🎯 Predict if stock outperforms S&P 500")

with col2:
    if 'raw' in data:
        st.metric("Total Data Points", f"{len(data['raw']):,}")
        st.metric("Date Range", f"{data['raw']['Date'].min().date()} to {data['raw']['Date'].max().date()}")

with col3:
    if 'ml' in data:
        st.metric("ML Features", len([c for c in data['ml'].columns if c not in ['Date', 'stock', 'y', 'stock_fwd_ret_21d', 'sp500_fwd_ret_21d']]))
        st.metric("Stocks Analyzed", len(data['ml']['stock'].unique()))

st.markdown("---")

# Pipeline overview
st.subheader("Data Pipeline")

pipeline_steps = [
    "1️⃣ **Data Collection**: 10+ data sources (stocks, macro, market indicators)",
    "2️⃣ **Data Integration**: Merge on (stock, Date) key",
    "3️⃣ **Data Cleaning**: Smart imputation + outlier removal",
    "4️⃣ **Feature Scaling**: StandardScaler, RobustScaler, MinMaxScaler",
    "5️⃣ **Feature Engineering**: 30+ technical/fundamental features",
    "6️⃣ **Model Training**: Random Forest, GBM, H2O AutoML",
    "7️⃣ **Evaluation**: Time-series split (80/20)"
]

for step in pipeline_steps:
    st.markdown(step)

st.markdown("---")
st.subheader(":material/api: APIs")
st.markdown('''The datasets used in this project were collected from a combination of financial, macroeconomic, and technical-analysis data providers. Together, they capture price behavior, market conditions, and economic context necessary to predict whether **META** will outperform the **S&P 500**. All sources were accessed through APIs using the Python libraries `yfinance`, `requests`, and `pandas`, and all data are time-aligned by the variable `Date`''')

st.subheader("📁 Data Sources Used")
    
sources = [
    {"Category": "Stock Prices", "Files": "GOOGL_raw.csv, META_raw.csv", "Records": "5,000+"},
    {"Category": "Benchmark", "Files": "^GSPC_raw.csv (S&P 500)", "Records": "5,000+"},
    {"Category": "Macro Data", "Files": "CPI, GDP, Fed Funds Rate, Unemployment", "Records": "200+"},
    {"Category": "Market Indicators", "Files": "VIX, Put/Call Ratio, Market Breadth", "Records": "1,000+"},
    {"Category": "Sector ETFs", "Files": "XLK, XLF, XLV, XLE, XLI", "Records": "1,000+"},
    {"Category": "Technical Indicators", "Files": "SPY/QQQ RSI, SMA 50/200", "Records": "1,000+"}
]

st.table(pd.DataFrame(sources))