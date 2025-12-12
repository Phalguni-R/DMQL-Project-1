"""
FMA Analytics Dashboard - Main Landing Page
Phase 3: DMQL Project
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="FMA Analytics Dashboard",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1DB954;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .feature-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<p class="main-header">🎵 FMA Analytics Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Explore Music Data from the Free Music Archive</p>', unsafe_allow_html=True)

# Introduction
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    ### Welcome to the FMA Analytics Dashboard!

    This interactive dashboard allows you to explore music data from the Free Music Archive (FMA) dataset.
    Navigate using the sidebar to access different analysis modules.
    """)

st.markdown("---")

# Dashboard modules overview
st.markdown("### 📊 Available Dashboards")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
    <h4>🎵 Music Discovery</h4>
    <ul>
        <li>Genre Radar Chart - Compare audio features across genres</li>
        <li>Artist Timeline - Track popularity over years</li>
        <li>Hidden Gems - Discover high-quality, low-listen tracks</li>
    </ul>
    <p><b>Navigate to Music Discovery in the sidebar →</b></p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
    <h4>🏢 Label & Market Analysis</h4>
    <ul>
        <li>Label Success - Top labels by metrics</li>
        <li>Genre Trends - Popularity heatmap over time</li>
        <li>Artist Distribution - Geographic visualization</li>
    </ul>
    <p><b>Navigate to Label Analysis in the sidebar →</b></p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
    <h4>📊 Track Performance</h4>
    <ul>
        <li>Performance Table - Sortable track metrics</li>
        <li>Feature Correlation - Audio feature relationships</li>
        <li>Top Tracks Treemap - Hierarchical visualization</li>
    </ul>
    <p><b>Navigate to Track Performance in the sidebar →</b></p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Project information
st.markdown("### 🔧 Tech Stack")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.info("**PostgreSQL**\nDatabase")
with col2:
    st.info("**dbt**\nData Modeling")
with col3:
    st.info("**Streamlit**\nVisualization")
with col4:
    st.info("**Docker**\nDeployment")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>DMQL Project - Phase 3 | Data Management & Query Languages</p>
    <p>Free Music Archive Analytics Dashboard</p>
</div>
""", unsafe_allow_html=True)
