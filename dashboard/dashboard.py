import code
import streamlit as st
import pandas as pd
from utils import load_data, get_tools_used
st.set_page_config(
    page_title="Stock Prediction Data Pipeline",
    page_icon="📊",
    layout="wide"
)

st.markdown("# Project Overview")

st.sidebar.success("Select a pipeline stage above.")
data = load_data()
    
st.metric("ML Task", "Binary Classification")
st.info("🎯 Predict whether an individual stock will outperform S&P 500 index over the next 21 days (~ 1 month)", width='stretch')
if 'raw' in data:
    st.metric("Date Range", f"{data['raw']['Date'].min().date()} to {data['raw']['Date'].max().date()}")
col1, col2, col3 = st.columns(3)
with col1:
    if 'raw' in data:
        st.metric("Total Data Points", f"{len(data['raw']):,}")
with col2:
    if 'ml' in data:
        st.metric("ML Features", len([c for c in data['ml'].columns if c not in ['Date', 'stock', 'y', 'stock_fwd_ret_21d', 'sp500_fwd_ret_21d']]))
with col3:
    if 'ml' in data:
        st.metric("Stocks Analyzed", len(data['ml']['stock'].unique()))

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
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
with col2: 
    st.subheader("Tools Used")
    tools_df = get_tools_used()
    simple_styled_df = tools_df.style.set_table_styles([{
        'selector': 'thead th',
        'props': [('background-color', '#f0f2f6'), 
                 ('font-weight', 'bold'),
                 ('border-bottom', '2px solid #4b8bbe')]
    }])
    st.dataframe(simple_styled_df, width="stretch", hide_index=True)
st.markdown("---")

st.header("Code Organization per Pipeline Stage")

# Data Collection
st.subheader("1️⃣ Data Collection")
st.caption("""`data.py` contains the RawDataCollector class which handles data collection from various sources
            
            """)
# data.py snippet RawDataCollector class
st.markdown("""**Snippet:**""")
raw_data_collector_snippet = '''
class RawDataCollector:
    def __init__(self, start_date=START_DATE, end_date=END_DATE, data_dir=DATA_DIR):
        self.start_date = start_date
        self.end_date = end_date or datetime.now().strftime('%Y-%m-%d')
        self.data_dir = data_dir

    # ---------- Yahoo Finance ----------
    def collect_yahoo(self, symbols):
        for symbol in symbols:
            print(f"Collecting {symbol} from Yahoo Finance...")
            try:
                df = yf.download(symbol, start=self.start_date, end=self.end_date, progress=False, auto_adjust=True)
                df.to_csv(f'{self.data_dir}/{symbol}_raw.csv')
            except Exception as e:
                print(f"Error collecting {symbol}: {e}")
    
    # ---------- FRED Economic Data ----------           
    def collect_fred(self, fred_series, api_key)
    
    # ---------- Alpha Vantage Technical Indicators ----------
    def collect_alpha_vantage(self, symbol, indicators)
    
    # ---------- Sentiment & Market Indicators ----------
    def collect_sentiment(self)
'''
st.code(raw_data_collector_snippet, language='python')
st.markdown("---")


# Data Integration
st.subheader("2️⃣ Data Integration")
# integrate_data.py snippet

# st.markdown("""**Scripts:**""" )
st.caption("`integrate_data.py` : Loads all raw CSV files, fixes MultiIndex issues, and integrates into one unified dataset. Each row represents a (stock, date) pair with all available raw data columns.")


# Data Cleaning
st.subheader("3️⃣ Data Cleaning")
# prepare_data.py snippet - imputation and outlier removal
# clean_ml_dataset.py snippet - removing null rows
st.caption("`prepare_data.py` : Imputation strategies (mean, median, forward-fill) and outlier removal techniques (IQR, Z-score) applied to raw dataset to create clean ML-ready dataset.")
st.caption("`clean_ml_dataset.py` : Further cleans the ML dataset by removing rows with any remaining null values after imputation.")

# Feature Scaling
st.subheader("4️⃣ Feature Scaling")
# scale_features.py snippet - StandardScaler, RobustScaler, MinMaxScaler
st.caption("`scale_features.py` : Applies appropriate scaling techniques (StandardScaler, RobustScaler, MinMaxScaler) to prepared dataset and documents all applied transformations.")

# Feature Engineering
st.subheader("5️⃣ Feature Engineering")
# create_features_and_label.py snippet
st.caption("`create_features_and_label.py` : Creates engineered features (X) and target variable (y) from integrated prepared data. Saves to a separate CSV file: `ml_features_and_labels.csv` ")

# Model Training & Results
st.subheader("6️⃣ Model Training & Results")

# jupyter notebook snippets for model training 
st.caption("**Traning Notebooks:**")
st.caption("`Logistic Regression Model.ipynb`")
st.caption("`Random Forest Model.ipynb`")
st.caption("`XGBoost Model.ipynb`")
# h20 automl model training snippet
# compare_models.py snippet
# compare_models_timeseries.py snippet
# compare_models_timeseries_gbm.py snippet
# compare_models_timeseries_ensemble.py snippet

# Performance Evaluation
st.subheader("7️⃣ Performance Evaluation")
st.caption("`compare_models.py` : Random Split Comparison (RF)")
st.caption("`compare_models_timeseries.py` : Time Series Comparison (RF)")
st.caption("`compare_models_timeseries_gbm.py` : Time Series Comparison (GBM)")
st.caption("`run_automl.py` : AutoML")
st.caption("`investigate_automl_leakage.py` : Helps discover H2O AutoML leakage: The 96.6% AUC was inflated due to it's default 5-fold Cross-Validation `(nfolds=5)` ")
st.caption("`investigate_overfitting.py` : Overfitting Investigation")
