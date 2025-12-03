import streamlit as st
import time
import numpy as np
import pandas as pd
import plotly.express as px
from utils import load_data

st.set_page_config(page_title="Data Cleaning", page_icon="🧹", layout="wide")
st.markdown("# Data Cleaning")
st.sidebar.header("Data Cleaning")
data = load_data()

# Show distribution before cleaning
# Null handling
st.header("Null Value Handling")

if 'raw' in data and 'prepared' in data:
    raw_nulls = data['raw'].isnull().sum().sum()
    prep_nulls = data['prepared'].isnull().sum().sum()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Nulls Before", f"{raw_nulls:,}")
    with col2:
        st.metric("Nulls After", f"{prep_nulls:,}")
    with col3:
        improvement = ((raw_nulls - prep_nulls) / raw_nulls * 100) if raw_nulls > 0 else 100
        st.metric("Improvement", f"{improvement:.1f}%")
    
    st.success('''**Strategy**: Smart imputation based on data type''')
    st.badge("Forward then backward fill for macroeconomic data", icon=":material/counter_1:", color="green")
    st.badge("Forward fill for stock prices", icon=":material/counter_2:", color="green")
    st.badge("Linear interpolation for scattered missing values", icon=":material/counter_3:", color="green")

# Data completeness bar chart
# st.subheader("Data Completeness Distribution")
if 'raw' in data:
    df = data['raw']
    null_pct = (df.isnull().sum() / len(df) * 100).sort_values(ascending=False)
    null_pct = null_pct[null_pct > 0]

    if len(null_pct) > 0:
        fig = px.bar(
            x=null_pct.index,
            y=null_pct.values,
            title="Missing Data per Column (%)",
            labels={'x': 'Column', 'y': 'Missing %'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, width='stretch')
    else:
        st.success("✅ No missing data in integrated dataset!")
    

# Outlier detection
st.subheader("Outlier Detection & Removal")
st.info("**Method**: Z-score Threshold = 3 standard deviations")

if 'outliers' in data:
    outlier_df = data['outliers']
    
    # Display outlier summary
    st.dataframe(outlier_df, width='stretch')
    
    # Visualization
    if 'column' in outlier_df.columns and 'zscore_outliers' in outlier_df.columns:
        top_outliers = outlier_df.nlargest(10, 'zscore_outliers')
        
        fig = px.bar(
            top_outliers,
            x='column',
            y='zscore_outliers',
            title='Top 10 Columns by Outliers Detected (Z-score > 3)',
            labels={'outliers_detected': 'Number of Outliers'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, width='stretch')

if 'raw' in data and 'prepared' in data:
    rows_before = len(data['raw'])
    rows_after = len(data['prepared'])
    removed = rows_before - rows_after
    
    # st.metric("Rows Removed", f"{removed:,} ({removed/rows_before*100:.2f}%)")