"""
Arun's Visualizations
- Genre Radar Chart
- Artist Geographic Heatmap
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys

import sys

sys.path.append('..')
from utils.db_connection import execute_query
from utils.queries import (
    get_genre_audio_features,
    get_available_genres,
    get_artist_geographic_data,
    get_year_range
)

# Page config
st.set_page_config(page_title="Arun's Visualizations", page_icon="🎯", layout="wide")

st.title("🎯 Arun's Visualizations")
st.markdown("Genre Radar Chart & Artist Geographic Heatmap")
st.markdown("---")

# ============================================
# VISUALIZATION 1: GENRE RADAR CHART
# ============================================

st.header("🎯 Genre Audio Features Comparison")
st.markdown("Compare audio characteristics across different music genres")

# Get available genres for dropdown
genres_df = execute_query(get_available_genres())

if not genres_df.empty:
    # Interactive filters in columns
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        # Multi-select for genres
        selected_genres = st.multiselect(
            "Select Genres to Compare",
            options=genres_df['genre_name'].tolist(),
            default=genres_df['genre_name'].head(5).tolist(),
            help="Choose 2-8 genres for best visualization"
        )

    with col2:
        # Feature selector
        all_features = [
            'avg_energy', 'avg_danceability', 'avg_valence',
            'avg_acousticness', 'avg_instrumentalness',
            'avg_liveness', 'avg_speechiness'
        ]
        selected_features = st.multiselect(
            "Select Audio Features",
            options=all_features,
            default=all_features[:5],
            help="Choose which features to display on radar chart"
        )

    with col3:
        # Min tracks slider
        min_tracks = st.slider(
            "Minimum Tracks per Genre",
            min_value=10,
            max_value=100,
            value=20,
            step=10,
            help="Filter out genres with too few tracks"
        )

    # Query data
    if selected_genres and selected_features:
        radar_df = execute_query(get_genre_audio_features(selected_genres))
        radar_df = radar_df[radar_df['track_count'] >= min_tracks]

        if not radar_df.empty:
            # Create radar chart
            fig = go.Figure()

            # Clean feature names for display
            feature_labels = [f.replace('avg_', '').title() for f in selected_features]

            for _, row in radar_df.iterrows():
                values = [row[feat] for feat in selected_features]

                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=feature_labels,
                    fill='toself',
                    name=f"{row['genre_name']} ({int(row['track_count'])} tracks)"
                ))

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )
                ),
                showlegend=True,
                title="Genre Audio Features Radar Chart",
                height=600
            )

            st.plotly_chart(fig, use_container_width=True)

            # Show data table
            with st.expander("📊 View Raw Data"):
                st.dataframe(radar_df, use_container_width=True)
        else:
            st.warning("⚠️ No genres found with the selected filters. Try lowering minimum tracks.")
    else:
        st.info("👆 Select genres and features above to generate the radar chart")
else:
    st.error("❌ Could not load genre data. Check database connection.")

st.markdown("---")

# ============================================
# VISUALIZATION 2: ARTIST GEOGRAPHIC HEATMAP
# ============================================

st.header("🗺️ Artist Geographic Distribution")
st.markdown("Explore where artists are located and their popularity across regions")

# Get year range for slider
year_range_df = execute_query(get_year_range())

if not year_range_df.empty:
    min_year = int(year_range_df.iloc[0]['min_year'])
    max_year = int(year_range_df.iloc[0]['max_year'])

    # Handle invalid years (0, NULL, or unrealistic values)
    if min_year < 1900 or min_year == 0:
        min_year = 1900
    if max_year > 2025 or max_year == 0:
        max_year = 2025
    if min_year >= max_year:
        min_year = 1900
        max_year = 2025

    # Interactive filters
    col1, col2 = st.columns([3, 1])

    with col1:
        # Year range slider
        year_range = st.slider(
            "Select Year Range",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year),
            help="Filter artists by their active year"
        )

    with col2:
        # Metric toggle
        metric_choice = st.radio(
            "Map Metric",
            options=["Artist Count", "Average Hotness"],
            help="Choose what to visualize on the map"
        )

    # Query geographic data
    geo_df = execute_query(get_artist_geographic_data(year_range[0], year_range[1]))

    if not geo_df.empty:
        # Remove any invalid coordinates
        geo_df = geo_df.dropna(subset=['artist_latitude', 'artist_longitude'])
        geo_df = geo_df[
            (geo_df['artist_latitude'].between(-90, 90)) &
            (geo_df['artist_longitude'].between(-180, 180))
            ]

        if not geo_df.empty:
            # Determine size/color metric
            if metric_choice == "Artist Count":
                size_col = 'track_count'
                color_col = 'track_count'
                hover_data = ['artist_name', 'artist_location', 'track_count']
            else:
                size_col = 'avg_hotness'
                color_col = 'avg_hotness'
                hover_data = ['artist_name', 'artist_location', 'avg_hotness']

            # Create scatter mapbox
            fig = px.scatter_mapbox(
                geo_df,
                lat='artist_latitude',
                lon='artist_longitude',
                size=size_col,
                color=color_col,
                hover_name='artist_name',
                hover_data=hover_data,
                color_continuous_scale='YlOrRd',
                size_max=15,
                zoom=1,
                title=f"Artist Distribution by {metric_choice} ({year_range[0]}-{year_range[1]})"
            )

            fig.update_layout(
                mapbox_style="open-street-map",
                height=600,
                margin={"r": 0, "t": 40, "l": 0, "b": 0}
            )

            st.plotly_chart(fig, use_container_width=True)

            # Summary statistics
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Artists", len(geo_df))
            col2.metric("Countries/Regions", geo_df['artist_location'].nunique())
            col3.metric("Avg Tracks per Artist", f"{geo_df['track_count'].mean():.1f}")
            col4.metric("Avg Hotness", f"{geo_df['avg_hotness'].mean():.3f}")

            # Top locations table
            with st.expander("📍 Top Locations"):
                location_stats = geo_df.groupby('artist_location').agg({
                    'artist_id': 'count',
                    'track_count': 'sum',
                    'avg_hotness': 'mean'
                }).reset_index()
                location_stats.columns = ['Location', 'Artist Count', 'Total Tracks', 'Avg Hotness']
                location_stats = location_stats.sort_values('Artist Count', ascending=False).head(10)
                st.dataframe(location_stats, use_container_width=True)
        else:
            st.warning("⚠️ No valid geographic data found for the selected year range.")
    else:
        st.warning("⚠️ No artist data found. Check database connection.")
else:
    st.error("❌ Could not load year range data.")

st.markdown("---")
st.caption("Arun's Visualizations | DMQL Phase 3")
