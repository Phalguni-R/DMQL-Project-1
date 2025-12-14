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

# ============================================
# VISUALIZATION 2: AUDIO FEATURES CORRELATION MATRIX
# ============================================

st.header("🔗 Audio Features Correlation Matrix")
st.markdown("Discover how different audio characteristics relate to each other")

# Genre filter
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    genres_df = execute_query(get_available_genres_simple())
    genre_options = ["All Genres"] + genres_df['genre_name'].tolist() if not genres_df.empty else ["All Genres"]
    selected_genre = st.selectbox(
        "Filter by Genre (optional)",
        options=genre_options,
        help="Analyze correlations for a specific genre"
    )

# Query data
corr_df = execute_query(get_audio_features_correlation(selected_genre if selected_genre != "All Genres" else None))

if not corr_df.empty and len(corr_df) > 10:
    # Calculate correlation matrix
    correlation_matrix = corr_df.corr()

    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=correlation_matrix.values,
        texttemplate='%{text:.2f}',
        textfont={"size": 10},
        colorbar=dict(title="Correlation")
    ))

    fig.update_layout(
        title=f"Audio Features Correlation - {selected_genre}",
        xaxis_title="",
        yaxis_title="",
        height=600,
        width=700
    )

    st.plotly_chart(fig, use_container_width=True)

    # Insights
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔍 Key Insights")

        # Find strongest positive correlation (excluding diagonal)
        corr_values = correlation_matrix.values
        import numpy as np
        np.fill_diagonal(corr_values, 0)
        max_corr_idx = np.unravel_index(np.argmax(corr_values), corr_values.shape)
        max_corr = corr_values[max_corr_idx]

        st.metric(
            "Strongest Positive Correlation",
            f"{correlation_matrix.columns[max_corr_idx[0]]} ↔ {correlation_matrix.columns[max_corr_idx[1]]}",
            f"{max_corr:.3f}"
        )

        # Find strongest negative correlation
        min_corr_idx = np.unravel_index(np.argmin(corr_values), corr_values.shape)
        min_corr = corr_values[min_corr_idx]

        st.metric(
            "Strongest Negative Correlation",
            f"{correlation_matrix.columns[min_corr_idx[0]]} ↔ {correlation_matrix.columns[min_corr_idx[1]]}",
            f"{min_corr:.3f}"
        )

    with col2:
        st.subheader("📊 Sample Statistics")
        st.metric("Tracks Analyzed", f"{len(corr_df):,}")
        st.metric("Features Compared", len(correlation_matrix.columns))

        # Average feature values
        with st.expander("📈 Average Feature Values"):
            avg_features = corr_df.mean().sort_values(ascending=False)
            st.dataframe(avg_features.to_frame(name='Average Value'), use_container_width=True)

else:
    st.warning("⚠️ Not enough data to calculate correlations. Try selecting 'All Genres' or a different genre.")

st.markdown("---")
st.caption("Phalguni's Visualizations | DMQL Phase 3")