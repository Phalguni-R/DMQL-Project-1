"""
Halle's Visualizations
TODO: Halle - Implement your 2 visualizations here
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
import pydeck as pdk
import numpy as np

# project_root = r"C:\Users\hb102\OneDrive\Documents\GitHub\DMQL-Project-1\streamlit_app"

# if project_root not in sys.path:
#     sys.path.insert(0, project_root)

sys.path.append('..')

from utils.db_connection import execute_query
from utils.queries_halle import (
    get_year_range, 
    get_top_genres_yearly,
    get_top_artists_yearly
)

# Page config
st.set_page_config(page_title="Halle's Visualizations", page_icon="🎭", layout="wide")

st.title("🎭 Halle's Visualizations")
st.markdown("---")

# ============================================
# VISUALIZATION 1 - Top Artists TL
# ============================================

st.header("📊 Top Artists Timeline")

# Graph filters
st.header("Artists Timeline Filter Settings")
    
# Year range filter
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

st.subheader("Year Range")
year_range = st.slider(
        "Select Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        help="Filter top artist visuals by date range",
        key="artist_year_range_slider"
        )
    
# Number of top genres to show
st.subheader("Display Settings")
top_n = st.slider(
        "Number of Top Artists to Display",
        min_value=1,
        max_value=10,
        value=3,
        help="Show top N artists per year"
    )
    
# Visualization type
st.subheader("Chart Type")
chart_type = st.selectbox(
        "Select Visualization",
        ["Line Chart","Heatmap"],
        help="Choose how to visualize the data",
        key = "artist_chart_select"
    )


st.markdown("---")
col1, col2 = st.columns([3, 1])

with col1:
    top_artist_df = execute_query(get_top_artists_yearly(year_range[0], year_range[1]))
    
    if not top_artist_df.empty:
        # Filter to top N artists
        top_artist_df = top_artist_df[top_artist_df['rank_in_year'] <= top_n]

        # Filter to selected range
        art_range_df = top_artist_df[
            (top_artist_df['release_year'] >= year_range[0]) & 
            (top_artist_df['release_year'] <= year_range[1])
            ].copy()

        art_summary_df = art_range_df.pivot_table(
            index='release_year',
            columns='artist_name',
            values='total_listens',
            aggfunc='sum'
        ).fillna(0)
        
        # Add total listens per year
        art_summary_df['Year_Total'] = art_summary_df.sum(axis=1)
        
        with col2:
            # Display summary statistics
            st.subheader("📊 Summary")
            
            # Total listens in period
            total_listens = int(art_summary_df.drop('Year_Total', axis=1).sum().sum())
            st.metric("Total Listens", f"{total_listens:,}")
            
            # Average per year
            avg_per_year = int(art_summary_df['Year_Total'].mean())
            st.metric("Avg Listens per Year", f"{avg_per_year:,}")
            
            # Number of unique genres
            unique_artists = art_range_df['artist_name'].nunique()
            st.metric("Unique Artists", unique_artists)
            
            # Most popular genre overall
            artist_totals = art_summary_df.drop('Year_Total', axis=1).sum().sort_values(ascending=False)
            if not artist_totals.empty:
                top_artist = artist_totals.index[0]
                top_artist_listens = int(artist_totals.iloc[0])
                st.metric("Top Artist", top_artist)
                st.metric(f"{top_artist} Listens", f"{top_artist_listens:,}")
            
            # Year with most listens
            top_year = art_summary_df['Year_Total'].idxmax()
            top_year_listens = int(art_summary_df.loc[top_year, 'Year_Total'])
            st.metric("Peak Year", top_year)
            st.metric(f"{top_year} Listens", f"{top_year_listens:,}")
        
        # Display the chart based on selected type
        st.subheader(f"📈 Top {top_n} Artists ({year_range[0]}-{year_range[1]})")

        # Calculating top N genres overall in the selected date range based on listens
        in_range_df = top_artist_df[
            (top_artist_df['release_year'] >= year_range[0]) & 
            (top_artist_df['release_year'] <= year_range[1])
            ].copy()

        artist_totals_in_range = in_range_df.groupby('artist_name')['total_listens'].sum().sort_values(ascending=False)
        top_n_artists = artist_totals_in_range.head(top_n).index.tolist()

        # Create filtered df with only top N genres in selected range for plots
        filtered_data = in_range_df[in_range_df['artist_name'].isin(top_n_artists)].copy()
           
        if chart_type == "Line Chart":

            # Create line chart
            line_df = filtered_data.pivot_table(
                index='release_year',
                columns='artist_name',
                values='total_listens'
            ).fillna(0)

            fig = px.line(
                line_df,
                markers=True,
                title=f'Artist Popularity Over Time ({year_range[0]}-{year_range[1]})'
            )
            
            fig.update_layout(
                height=500,
                xaxis_title="Year",
                yaxis_title="Total Listens",
                hovermode='x unified',
                xaxis=dict(
                    range=[year_range[0] - 0.5, year_range[1] + 0.5],
                    tickmode='array',
                    tick0=year_range[0],
                    tickvals=np.linspace(year_range[0], year_range[1], 5).astype(int),
                    showgrid=False
                )
            )
            
        elif chart_type == "Heatmap":
            # Create heatmap
            heatmap_data = filtered_data.pivot_table(
                index='artist_name',
                columns='release_year',
                values='rank_in_year'
            )

            # Sort by average rank
            heatmap_data['avg_rank'] = heatmap_data.mean(axis=1)
            heatmap_data = heatmap_data.sort_values('avg_rank').drop('avg_rank', axis=1)         

            fig = go.Figure(data=go.Heatmap(
                z=heatmap_data.values,
                x=heatmap_data.columns,
                y=heatmap_data.index,
                colorscale='Viridis',
                hoverongaps=False,
                colorbar=dict(title="Rank (1=Most popular)")
            ))
            
            fig.update_layout(
                height=600,
                title=f'Artist Rankings Heatmap ({year_range[0]}-{year_range[1]})',
                xaxis_title="Year",
                yaxis_title="Artist",
                xaxis=dict(
                    range=[year_range[0] - 0.5, year_range[1] + 0.5],
                    tickmode='array',
                    tick0=year_range[0],
                    tickvals=np.linspace(year_range[0], year_range[1], 5).astype(int),
                    showgrid=False
                )
            )
            
        # Display the chart
        st.plotly_chart(fig, use_container_width=True)
        
        # Display data table
        with st.expander("📋 View Raw Artist Popularity Data"):
            display_cols = ['release_year', 'artist_name', 'total_listens', 'rank_in_year']
            st.dataframe(
                top_artist_df[display_cols].sort_values(['release_year', 'rank_in_year']),
                use_container_width=True,
                height=300
            )



# ============================================
# VISUALIZATION 2 - Genre Trends over Time 
# ============================================

st.header("📊 Genre Trends Timeline")
st.markdown("Explore musical trends over time")

# Graph filters
st.header("Genre Timeline Filter Settings")
    
# Year range filter
st.subheader("Year Range")
year_range = st.slider(
        "Select Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        help="Filter genre popularity by date range",
        key="genre_year_range_slider"
        )
    
# Number of top genres to show
st.subheader("Display Settings")
top_n = st.slider(
        "Number of Top Genres to Display",
        min_value=3,
        max_value=20,
        value=10,
        help="Show top N genres per year"
    )
    
# Visualization type
st.subheader("Chart Type")
chart_type = st.selectbox(
        "Select Visualization",
        ["Line Chart", "Stacked Area", "Heatmap"],
        help="Choose how to visualize the data",
        key = "genre_chart_select"
    )


st.markdown("---")
col1, col2 = st.columns([3, 1])

with col1:
    top_genre_df = execute_query(get_top_genres_yearly(year_range[0], year_range[1]))
    
    if not top_genre_df.empty:
        # Filter to top N genres
        top_genre_df = top_genre_df[top_genre_df['yr_rank'] <= top_n]

        # Filter to selected range
        range_summary_df = top_genre_df[
            (top_genre_df['release_year'] >= year_range[0]) & 
            (top_genre_df['release_year'] <= year_range[1])
            ].copy()

        summary_df = range_summary_df.pivot_table(
            index='release_year',
            columns='genre_name',
            values='total_listens',
            aggfunc='sum'
        ).fillna(0)
        
        # Add total listens per year
        summary_df['Year_Total'] = summary_df.sum(axis=1)
        
        with col2:
            # Display summary statistics
            st.subheader("📊 Summary")
            
            # Total listens in period
            total_listens = int(summary_df.drop('Year_Total', axis=1).sum().sum())
            st.metric("Total Listens", f"{total_listens:,}")
            
            # Average per year
            avg_per_year = int(summary_df['Year_Total'].mean())
            st.metric("Avg Listens per Year", f"{avg_per_year:,}")
            
            # Number of unique genres
            unique_genres = range_summary_df['genre_name'].nunique()
            st.metric("Unique Genres", unique_genres)
            
            # Most popular genre overall
            genre_totals = summary_df.drop('Year_Total', axis=1).sum().sort_values(ascending=False)
            if not genre_totals.empty:
                top_genre = genre_totals.index[0]
                top_genre_listens = int(genre_totals.iloc[0])
                st.metric("Top Genre", top_genre)
                st.metric(f"{top_genre} Listens", f"{top_genre_listens:,}")
            
            # Year with most listens
            top_year = summary_df['Year_Total'].idxmax()
            top_year_listens = int(summary_df.loc[top_year, 'Year_Total'])
            st.metric("Peak Year", top_year)
            st.metric(f"{top_year} Listens", f"{top_year_listens:,}")
        
        # Display the chart based on selected type
        st.subheader(f"📈 Top {top_n} Genres ({year_range[0]}-{year_range[1]})")

        # Calculating top N genres overall in the selected date range based on listens
        in_range_df = top_genre_df[
            (top_genre_df['release_year'] >= year_range[0]) & 
            (top_genre_df['release_year'] <= year_range[1])
            ].copy()

        genre_totals_in_range = in_range_df.groupby('genre_name')['total_listens'].sum().sort_values(ascending=False)
        top_n_genres = genre_totals_in_range.head(top_n).index.tolist()

        # Create filtered df with only top N genres in selected range for plots
        filtered_data = in_range_df[in_range_df['genre_name'].isin(top_n_genres)].copy()
           
        if chart_type == "Line Chart":

            # Create line chart
            line_df = filtered_data.pivot_table(
                index='release_year',
                columns='genre_name',
                values='total_listens'
            ).fillna(0)

            fig = px.line(
                line_df,
                markers=True,
                title=f'Genre Popularity Over Time ({year_range[0]}-{year_range[1]})'
            )
            
            fig.update_layout(
                height=500,
                xaxis_title="Year",
                yaxis_title="Total Listens",
                hovermode='x unified',
                xaxis=dict(
                    range=[year_range[0] - 0.5, year_range[1] + 0.5],
                    tickmode='array',
                    tick0=year_range[0],
                    tickvals=np.linspace(year_range[0], year_range[1], 5).astype(int),
                    showgrid=False
                )
            )
            
        elif chart_type == "Heatmap":
            # Create heatmap
            heatmap_data = filtered_data.pivot_table(
                index='genre_name',
                columns='release_year',
                values='yr_rank'
            )

            # Sort by average rank
            heatmap_data['avg_rank'] = heatmap_data.mean(axis=1)
            heatmap_data = heatmap_data.sort_values('avg_rank').drop('avg_rank', axis=1)         

            fig = go.Figure(data=go.Heatmap(
                z=heatmap_data.values,
                x=heatmap_data.columns,
                y=heatmap_data.index,
                colorscale='Viridis',
                hoverongaps=False,
                colorbar=dict(title="Rank (1=Most popular)")
            ))
            
            fig.update_layout(
                height=600,
                title=f'Genre Rankings Heatmap ({year_range[0]}-{year_range[1]})',
                xaxis_title="Year",
                yaxis_title="Genre",
                xaxis=dict(
                    range=[year_range[0] - 0.5, year_range[1] + 0.5],
                    tickmode='array',
                    tick0=year_range[0],
                    tickvals=np.linspace(year_range[0], year_range[1], 5).astype(int),
                    showgrid=False
                )
            )
            
        else:  # Stacked Area
            area_df = filtered_data.pivot_table(
                index='release_year',
                columns='genre_name',
                values='total_listens'
            ).fillna(0)

            
            fig = px.area(
                area_df,
                title=f'Genre Market Share Over Time ({year_range[0]}-{year_range[1]})'
            )
            
            fig.update_layout(
                height=500,
                xaxis_title="Year",
                yaxis_title="Total Listens",
                hovermode='x unified',
                xaxis=dict(
                    range=[year_range[0] - 0.5, year_range[1] + 0.5],
                    tickmode='array',
                    tick0=year_range[0],
                    tickvals=np.linspace(year_range[0], year_range[1], 5).astype(int),
                    showgrid=False
                )            
            )
        
        # Display the chart
        st.plotly_chart(fig, use_container_width=True)
        
        # Display data table
        with st.expander("📋 View Raw Top Genre Data"):
            display_cols = ['release_year', 'genre_name', 'total_listens', 'yr_rank']
            st.dataframe(
                top_genre_df[display_cols].sort_values(['release_year', 'yr_rank']),
                use_container_width=True,
                height=300
            )
