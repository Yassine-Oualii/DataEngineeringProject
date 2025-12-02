import streamlit as st
import time
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from utils import load_data

st.set_page_config(page_title="Performance Analysis", page_icon="📈", layout="wide")
st.markdown("# Performance Analysis")
st.sidebar.header("Performance Analysis")
data = load_data()
st.subheader("Key Findings")
    
col1, col2 = st.columns(2)

with col1:
    st.success("✅ **Random Forest Best**: 51.8% (All Combined)")
    st.info("💡 Benefits from combining all data prep techniques")

with col2:
    st.success("✅ **GBM Best**: 51.9% (Scaled Data Only)")
    st.info("💡 Performs best with scaling alone")

st.markdown("---")

# Comparison chart
if 'rf_results' in data and 'gbm_results' in data:
    st.subheader("Model Comparison by Data Prep Scenario")
    
    # Merge results
    rf = data['rf_results'].copy()
    gbm = data['gbm_results'].copy()
    
    rf['Model'] = 'Random Forest'
    gbm['Model'] = 'GBM'
    
    # Align columns
    if 'AUC' not in rf.columns:
        rf['AUC'] = rf['Accuracy']  # Use accuracy as proxy
    
    combined = pd.concat([
        rf[['Scenario', 'Accuracy', 'Model']],
        gbm[['Scenario', 'Accuracy', 'Model']]
    ])
    
    fig = px.bar(
        combined,
        x='Scenario',
        y='Accuracy',
        color='Model',
        barmode='group',
        title='Random Forest vs GBM: Accuracy by Data Prep Strategy',
        color_discrete_map={'Random Forest': '#636EFA', 'GBM': '#EF553B'}
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, width='stretch')

st.markdown("---")

# Key insights
st.subheader("📊 Data Preparation Impact")

insights = [
    {"Technique": "Smart Imputation", "Impact": "Minimal (-0.6%)", "Insight": "Basic filling vs smart strategies"},
    {"Technique": "Outlier Removal", "Impact": "Slight Negative (-0.8%)", "Insight": "Removed valuable volatility signals"},
    {"Technique": "Feature Scaling", "Impact": "Positive (+1.6%)", "Insight": "Most effective single technique"},
    {"Technique": "All Combined", "Impact": "Best Overall (+3%)", "Insight": "Synergistic effect for Random Forest"}
]

st.table(pd.DataFrame(insights))

st.success("""
**Key Takeaway**: Scaling is the most critical data preparation step for this time-series prediction task. 
While Random Forest benefits from combining all techniques (51.8%), GBM achieves similar performance (51.9%) 
with scaling alone, suggesting diminishing returns from additional preprocessing.
""")

st.markdown("---")

# Data Preparation Evolution Timeline
st.subheader("📅 Data Preparation Evolution & Impact")

if 'rf_results' in data:
    # Create timeline of data prep stages
    timeline_data = [
        {"Stage": "Baseline", "Accuracy_RF": data['rf_results'].loc[0, 'Accuracy'], "Description": "Simple filling only"},
        {"Stage": "+ Smart Imputation", "Accuracy_RF": data['rf_results'].loc[1, 'Accuracy'], "Description": "Advanced null handling"},
        {"Stage": "+ Outlier Removal", "Accuracy_RF": data['rf_results'].loc[2, 'Accuracy'], "Description": "Z-score > 3 removed"},
        {"Stage": "+ Feature Scaling", "Accuracy_RF": data['rf_results'].loc[3, 'Accuracy'], "Description": "Standardization applied"},
        {"Stage": "All Combined", "Accuracy_RF": data['rf_results'].loc[4, 'Accuracy'], "Description": "Complete pipeline"}
    ]
    
    timeline_df = pd.DataFrame(timeline_data)
    
    # Add cumulative improvement
    baseline_acc = timeline_df['Accuracy_RF'].iloc[0]
    timeline_df['Improvement'] = (timeline_df['Accuracy_RF'] - baseline_acc) * 100
    
    # Create step chart
    fig_timeline = go.Figure()
    
    fig_timeline.add_trace(go.Scatter(
        x=timeline_df['Stage'],
        y=timeline_df['Accuracy_RF'],
        mode='lines+markers+text',
        text=[f"{acc:.2%}" for acc in timeline_df['Accuracy_RF']],
        textposition="top center",
        line=dict(width=4, color='#636EFA'),
        marker=dict(size=10, color='white', line=dict(width=2, color='#636EFA')),
        name="Random Forest Accuracy"
    ))
    
    # Add GBM if available
    if 'gbm_results' in data:
        gbm_accuracies = data['gbm_results']['Accuracy'].values
        fig_timeline.add_trace(go.Scatter(
            x=timeline_df['Stage'],
            y=gbm_accuracies,
            mode='lines+markers',
            line=dict(width=3, color='#EF553B', dash='dash'),
            marker=dict(size=8, color='white', line=dict(width=2, color='#EF553B')),
            name="GBM Accuracy"
        ))
    
    fig_timeline.update_layout(
        title="Model Performance Evolution with Data Preparation",
        xaxis_title="Data Preparation Stage",
        yaxis_title="Accuracy",
        height=500,
        hovermode='x unified',
        yaxis=dict(tickformat=".0%", range=[0.45, 0.55])  # Adjusted range for your data
    )
    
    st.plotly_chart(fig_timeline, width='stretch')
    
    # Improvement bar chart
    fig_improvement = px.bar(
        timeline_df,
        x='Stage',
        y='Improvement',
        title="Cumulative Improvement Over Baseline",
        text='Improvement',
        color='Improvement',
        color_continuous_scale='RdYlGn'
    )
    fig_improvement.update_traces(
        texttemplate='%{text:.2f}%',
        textposition='outside'
    )
    fig_improvement.update_layout(
        height=400,
        xaxis_title="Data Preparation Stage",
        yaxis_title="Improvement (%)"
    )
    st.plotly_chart(fig_improvement, width='stretch')