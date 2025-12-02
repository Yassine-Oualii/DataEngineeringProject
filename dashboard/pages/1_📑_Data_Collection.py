import streamlit as st
import time
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="Data Collection",
    page_icon="📑",
    layout="wide"
)
st.markdown("# Data Collection")
st.sidebar.header("Data Collection")

st.subheader(":material/api: APIs")


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