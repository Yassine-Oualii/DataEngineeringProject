"""
Utility functions for the Stock Prediction Dashboard
"""

import streamlit as st
import pandas as pd
import os
from functools import lru_cache

@st.cache_data
def load_data():
    """Load all datasets with caching"""
    data = {}
    
    # Raw data
    if os.path.exists('../data/integrated_raw_data.csv'):
        data['raw'] = pd.read_csv('../data/integrated_raw_data.csv')
        data['raw']['Date'] = pd.to_datetime(data['raw']['Date'])
    
    # Prepared data
    if os.path.exists('../data/integrated_prepared_data.csv'):
        data['prepared'] = pd.read_csv('../data/integrated_prepared_data.csv')
        data['prepared']['Date'] = pd.to_datetime(data['prepared']['Date'])
    
    # ML dataset
    if os.path.exists('../data/ml_features_and_labels_clean.csv'):
        data['ml'] = pd.read_csv('../data/ml_features_and_labels_clean.csv')
        data['ml']['Date'] = pd.to_datetime(data['ml']['Date'])
    
    # Model results
    if os.path.exists('../data/model_comparison_timeseries_results.csv'):
        data['rf_results'] = pd.read_csv('../data/model_comparison_timeseries_results.csv')
    
    if os.path.exists('../data/model_comparison_timeseries_gbm_results.csv'):
        data['gbm_results'] = pd.read_csv('../data/model_comparison_timeseries_gbm_results.csv')
    
    # Outlier analysis
    if os.path.exists('../data/outlier_detection_summary.csv'):
        data['outliers'] = pd.read_csv('../data/outlier_detection_summary.csv')
    
    # Scaling log
    if os.path.exists('../data/scaling_log.csv'):
        data['scaling'] = pd.read_csv('../data/scaling_log.csv')
    
    return data

def get_data():
    """Get loaded data with session state caching"""
    if 'data' not in st.session_state:
        st.session_state.data = load_data()
    return st.session_state.data

def create_page_header(title):
    """Create a consistent page header"""
    st.header(title)
    st.markdown("---")