import streamlit as st
import time
import numpy as np
import pandas as pd
from utils import load_data
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Feature Scaling", page_icon="⚖️", layout="wide")
st.markdown("# Feature Scaling")
st.sidebar.header("Feature Scaling")

data = load_data()

st.header("Feature Scaling & Normalization")
    
if 'scaling' in data:
    scaling_df = data['scaling']
    
    st.subheader("Scaling Strategies")
    
    # Group by scaler
    if 'scaler' in scaling_df.columns:
        scaler_counts = scaling_df['scaler'].value_counts()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("StandardScaler", scaler_counts.get('StandardScaler', 0))
            st.caption("For normally distributed features")
        
        with col2:
            st.metric("RobustScaler", scaler_counts.get('RobustScaler', 0))
            st.caption("For features with outliers")
        
        with col3:
            st.metric("MinMaxScaler", scaler_counts.get('MinMaxScaler', 0))
            st.caption("For bounded features")
    
    # Display scaling log
    st.subheader("Scaling Details")
    st.dataframe(scaling_df, width='stretch')
    
    # Before/After comparison (if available)
    if 'mean_before' in scaling_df.columns and 'mean_after' in scaling_df.columns:
        st.subheader("Mean Normalization Effect")
        
        fig = make_subplots(rows=1, cols=2, subplot_titles=["Before Scaling", "After Scaling"])
        
        # Before
        fig.add_trace(
            go.Bar(x=scaling_df['column'][:10], y=scaling_df['mean_before'][:10], name="Before"),
            row=1, col=1
        )
        
        # After
        fig.add_trace(
            go.Bar(x=scaling_df['column'][:10], y=scaling_df['mean_after'][:10], name="After"),
            row=1, col=2
        )
        
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, width='stretch')

