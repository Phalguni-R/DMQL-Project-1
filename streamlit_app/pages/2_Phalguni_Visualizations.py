"""
Phalguni's Visualizations
TODO: Phalguni - Implement your 2 visualizations here
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
sys.path.append('..')
from utils.db_connection import execute_query

from utils.queries_phalguni import (
    get_hidden_gems_data,
    get_audio_features_correlation,
    get_available_genres_simple
)

# Page config
st.set_page_config(page_title="Phalguni's Visualizations", page_icon="🎨", layout="wide")

st.title("🎨 Phalguni's Visualizations")
st.markdown("Hidden Gems Discovery & Audio Features Analysis")
st.markdown("---")

# ============================================
# VISUALIZATION 1: HIDDEN GEMS SCATTER PLOT
# ============================================

st.header("💎 Hidden Gems Discovery")
st.markdown("Find high-quality tracks with low listen counts - the undiscovered treasures!")

# Controls
col1, col2 = st.columns([1, 1])

with col1:
    min_hotness = st.slider(
        "Minimum Quality (Hotness)",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.1,
        help="Higher = better quality tracks"
    )

with col2:
    max_listens = st.slider(
        "Maximum Listens",
        min_value=1000,
        max_value=50000,
        value=10000,
        step=1000,
        help="Lower = more 'hidden' gems"
    )

# Query data
gems_df = execute_query(get_hidden_gems_data(min_hotness, max_listens))

if not gems_df.empty:
    # Create scatter plot
    fig = px.scatter(
        gems_df,
        x='listens',
        y='song_hotttnesss',
        color='genre_name',
        size='energy',
        hover_name='track_name',
        hover_data={
            'artist_name': True,
            'listens': ':,',
            'song_hotttnesss': ':.3f',
            'genre_name': True,
            'energy': ':.2f',
            'danceability': ':.2f',
            'valence': ':.2f'
        },
        title=f"Hidden Gems: High Quality ({min_hotness}+) with Low Listens (<{max_listens:,})",
        labels={
            'listens': 'Total Listens',
            'song_hotttnesss': 'Track Quality (Hotness)',
            'genre_name': 'Genre'
        },
        height=600
    )

    fig.update_layout(
        xaxis_type='log',
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    # Summary stats
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Hidden Gems Found", len(gems_df))
    col2.metric("Avg Quality", f"{gems_df['song_hotttnesss'].mean():.3f}")
    col3.metric("Avg Listens", f"{gems_df['listens'].mean():,.0f}")
    col4.metric("Genres", gems_df['genre_name'].nunique())

    # Top hidden gems table
    with st.expander("🏆 Top Hidden Gems"):
        top_gems = gems_df.nlargest(20, 'song_hotttnesss')[['track_name', 'artist_name', 'genre_name', 'song_hotttnesss', 'listens']].copy()
        top_gems.columns = ['Track', 'Artist', 'Genre', 'Quality', 'Listens']
        top_gems.index = range(1, len(top_gems) + 1)
        st.dataframe(top_gems, use_container_width=True)
else:
    st.warning("⚠️ No hidden gems found with these filters. Try adjusting the sliders.")

st.markdown("---")