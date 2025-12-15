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

    This interactive dashboard provides deep insights into music data from the Free Music Archive (FMA),
    built on a modern data stack with PostgreSQL, dbt, and Docker.
    
    **Available Visualizations:**
    
    **🎯 Arun's Visualizations:**
    - **Genre Radar Chart** - Compare audio features (energy, danceability, acousticness, etc.) across different music genres using sports-style analytics
    - **Artist Geographic Heatmap** - Explore where artists are located worldwide and their popularity by region
    - **Artist Popularity Timeline** - Watch top artists rise and fall through the years with an animated bar chart race
    
    **🎨 Phalguni's Visualizations:**
    - **Hidden Gems Discovery** - Find high-quality tracks with low listen counts - undiscovered musical treasures
    - **Audio Features Correlation Matrix** - Discover how different audio characteristics relate to each other
    
    **🎭 Halle's Visualizations:**
    - **Artist Popularity Timeline** - See the top artists in the FMA database during a fixed period of time
    - **Genre Trend Timeline** - Explore musical genre trends over time
    
    Use the sidebar to navigate between different visualizations.
    """)

st.markdown("---")

# Tech Stack
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
    <p>16,916 Artists • 95,557 Tracks • 162 Genres</p>
</div>
""", unsafe_allow_html=True)
