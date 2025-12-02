import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import get_data, create_page_header

st.set_page_config(
    page_title="Feature Importance",
    page_icon="⭐",
    layout="wide"
)

create_page_header("⭐ Feature Importance Analysis")

data = get_data()

if not data or ('rf_results' not in data and 'gbm_results' not in data):
    st.warning("No model results available. Please train models first.")
else:
    st.subheader("Model Performance Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Random Forest Results")
        if 'rf_results' in data:
            rf_df = data['rf_results']
            st.dataframe(rf_df.head(10), use_container_width=True)
            
            # Feature importance visualization
            if 'feature_importance' in rf_df.columns:
                fig, ax = plt.subplots(figsize=(10, 6))
                importance_counts = rf_df['feature_importance'].value_counts().head(10)
                importance_counts.plot(kind='barh', ax=ax, color='steelblue')
                ax.set_xlabel('Frequency')
                ax.set_title('Top 10 Important Features - Random Forest')
                ax.invert_yaxis()
                st.pyplot(fig)
        else:
            st.info("Random Forest results not available")
    
    with col2:
        st.subheader("Gradient Boosting Results")
        if 'gbm_results' in data:
            gbm_df = data['gbm_results']
            st.dataframe(gbm_df.head(10), use_container_width=True)
            
            # Feature importance visualization
            if 'feature_importance' in gbm_df.columns:
                fig, ax = plt.subplots(figsize=(10, 6))
                importance_counts = gbm_df['feature_importance'].value_counts().head(10)
                importance_counts.plot(kind='barh', ax=ax, color='darkgreen')
                ax.set_xlabel('Frequency')
                ax.set_title('Top 10 Important Features - Gradient Boosting')
                ax.invert_yaxis()
                st.pyplot(fig)
        else:
            st.info("Gradient Boosting results not available")
    
    st.markdown("---")
    
    st.subheader("📊 Feature Importance Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    if 'rf_results' in data:
        rf_count = len(data['rf_results'])
        with col1:
            st.metric("RF Records", rf_count)
    
    if 'gbm_results' in data:
        gbm_count = len(data['gbm_results'])
        with col2:
            st.metric("GBM Records", gbm_count)
    
    with col3:
        st.metric("Models Compared", "2")
    
    st.markdown("---")
    
    # Detailed Feature Analysis
    st.subheader("🔍 Detailed Feature Analysis")
    
    model_choice = st.radio("Select model:", ["Random Forest", "Gradient Boosting"])
    
    if model_choice == "Random Forest" and 'rf_results' in data:
        df_choice = data['rf_results']
    elif model_choice == "Gradient Boosting" and 'gbm_results' in data:
        df_choice = data['gbm_results']
    else:
        st.warning("Selected model data not available")
        df_choice = None
    
    if df_choice is not None:
        st.dataframe(df_choice, use_container_width=True)
        
        # Download option
        csv = df_choice.to_csv(index=False)
        st.download_button(
            label=f"Download {model_choice} Results",
            data=csv,
            file_name=f"{model_choice.lower()}_results.csv",
            mime="text/csv"
        )