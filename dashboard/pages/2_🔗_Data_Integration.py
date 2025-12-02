import streamlit as st
import time
import numpy as np
import pandas as pd
import plotly.express as px
from utils import load_data

st.set_page_config(page_title="Data Integration", page_icon="🔗", layout="wide")
st.markdown("# Data Integration")
st.sidebar.header("Data Integration")

data = load_data()

st.header("Data Integration & Schema")
    
if 'raw' in data:
    df = data['raw']

    # Schema overview
    st.subheader("Integrated Schema")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Columns", len(df.columns))
        st.metric("Primary Key", "(stock, Date)")

    with col2:
        st.metric("Total Rows", f"{len(df):,}")
        st.metric("Null Values", f"{df.isnull().sum().sum():,}")

    # Column breakdown
    st.subheader("Column Categories")

    categories = {
        "Stock Data (OHLCV)": ["Close", "High", "Low", "Open", "Volume"],
        "S&P 500 Benchmark": [c for c in df.columns if c.startswith('sp500_')],
        "Macro Indicators": ["CPI", "GDP", "Fed_Funds_Rate", "Unemployment_Rate"],
        "Market Indicators": ["VIX", "Put_Call_Ratio", "Market_Breadth"],
        "Sector ETFs": [c for c in df.columns if c.startswith('sector_')],
        "Technical Indicators": [c for c in df.columns if 'RSI' in c or 'SMA' in c]
    }

    for category, cols in categories.items():
        matching_cols = [c for c in cols if c in df.columns]
        if matching_cols:
            with st.expander(f"**{category}** ({len(matching_cols)} columns)"):
                st.write(", ".join(matching_cols))

    # Enhanced Time Series Analysis
    st.subheader("📈 Time Series Trends")

    col1, col2 = st.columns(2)

    with col1:
        # Select stocks for analysis
        stocks = df['stock'].unique()[:5]  # Limit to first 5 stocks for clarity
        selected_stocks = st.multiselect(
            "Select stocks for analysis",
            stocks,
            default=stocks[:2]
        )

    with col2:
        # Select time period
        date_range = st.date_input(
            "Select date range",
            [df['Date'].min().date(), df['Date'].max().date()]
        )

    if selected_stocks and len(date_range) == 2:
        # Filter data
        mask = (df['stock'].isin(selected_stocks)) & \
                (df['Date'] >= pd.to_datetime(date_range[0])) & \
                (df['Date'] <= pd.to_datetime(date_range[1]))
        filtered_df = df[mask]
        
                    # Simple price comparison
        fig = px.line(
            filtered_df,
            x='Date',
            y='Close',
            color='stock',
            title=f'Stock Prices: {date_range[0]} to {date_range[1]}'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, width='stretch')
        
        # Simple correlation heatmap
        try:
            pivot_data = filtered_df.pivot_table(
                index='Date',
                columns='stock',
                values='Close'
            ).dropna()
            
            if len(pivot_data.columns) > 1:
                correlation_matrix = pivot_data.corr()
                
                fig_corr = px.imshow(
                    correlation_matrix,
                    text_auto=True,
                    aspect="auto",
                    color_continuous_scale='RdBu_r',
                    title="Stock Price Correlations",
                    zmin=-1,
                    zmax=1
                )
                # show annotations and format values to two decimals
                fig_corr.update_traces(texttemplate='%{z:.2f}', textfont={'size':12})
                fig_corr.update_layout(height=400)
                st.plotly_chart(fig_corr, width='stretch')
        except:
            st.info("Could not create correlation matrix")

    # Data completeness heatmap
    st.subheader("Data Completeness by Source")

    null_pct = (df.isnull().sum() / len(df) * 100).sort_values(ascending=False)
    null_pct = null_pct[null_pct > 0]

    if len(null_pct) > 0:
        fig = px.bar(
            x=null_pct.index,
            y=null_pct.values,
            title="Missing Data by Column (%)",
            labels={'x': 'Column', 'y': 'Missing %'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, width='stretch')
    else:
        st.success("✅ No missing data in integrated dataset!")

    st.markdown("---")