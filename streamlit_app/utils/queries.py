"""
SQL Queries for Dashboard Visualizations
All queries use dbt analytics tables for optimal performance
"""


# ============================================
# MUSIC DISCOVERY PAGE QUERIES
# ============================================

def get_genre_audio_features(selected_genres: list = None):
    """
    Query for Genre Radar Chart
    Fetches average audio features for selected genres from dbt mart
    """
    if selected_genres and len(selected_genres) > 0:
        genre_list = "', '".join(selected_genres)
        where_clause = f"WHERE genre_name IN ('{genre_list}')"
    else:
        where_clause = ""

    query = f"""
    SELECT 
        genre_name,
        avg_acousticness,
        avg_danceability,
        avg_energy,
        avg_instrumentalness,
        avg_liveness,
        avg_speechiness,
        avg_valence,
        track_count
    FROM analytics.mart_genre_profiles
    {where_clause}
    ORDER BY track_count DESC;
    """
    return query


def get_available_genres():
    """
    Get list of all available genres for dropdown filter
    """
    query = """
    SELECT DISTINCT genre_name
    FROM analytics.mart_genre_profiles
    WHERE track_count > 10
    ORDER BY genre_name;
    """
    return query


def get_artist_geographic_data(year_start: int = None, year_end: int = None):
    """
    Query for Artist Geographic Heatmap
    Fetches artist location data (latitude, longitude) with metrics
    """
    year_filter = ""
    if year_start and year_end:
        year_filter = f"WHERE artist_active_year_begin BETWEEN {year_start} AND {year_end}"

    query = f"""
    SELECT 
        a.artist_id,
        a.artist_name,
        a.artist_latitude,
        a.artist_longitude,
        a.artist_location,
        a.artist_active_year_begin,
        COUNT(DISTINCT t.track_id) as track_count,
        COALESCE(AVG(s.song_hotttnesss), 0) as avg_hotness
    FROM analytics.dim_artists a
    LEFT JOIN public."Tracks" t ON a.artist_id = t.artist_id
    LEFT JOIN public."Social" s ON t.track_id = s.track_id
    {year_filter}
    GROUP BY a.artist_id, a.artist_name, a.artist_latitude, a.artist_longitude, 
             a.artist_location, a.artist_active_year_begin
    HAVING a.artist_latitude IS NOT NULL 
       AND a.artist_longitude IS NOT NULL
    ORDER BY avg_hotness DESC;
    """
    return query


# TODO: TEAMMATE 1 - Artist Timeline Query
def get_artist_timeline_data():
    """
    PLACEHOLDER for Artist Timeline visualization
    Query should fetch top artists' popularity metrics over years

    Expected columns:
    - year
    - artist_name
    - total_listens OR popularity_score
    - track_count
    """
    query = """
    -- TODO: TEAMMATE 1 - Implement this query
    -- Hint: Use analytics.mart_top_artists_yearly table
    -- Should show artist popularity trends across years
    SELECT 
        'PLACEHOLDER' as year,
        'PLACEHOLDER' as artist_name,
        0 as popularity_score
    LIMIT 1;
    """
    return query


# TODO: TEAMMATE 2 - Hidden Gems Query
def get_hidden_gems_data(min_hotness: float = 0.5, max_listens: int = 1000):
    """
    PLACEHOLDER for Hidden Gems scatter plot
    Query should find high-quality tracks with low listen counts

    Expected columns:
    - track_name
    - artist_name
    - song_hotttnesss
    - listens
    - audio features (energy, danceability, etc.)
    """
    query = f"""
    -- TODO: TEAMMATE 2 - Implement this query
    -- Hint: Use analytics.mart_undiscovered_gems table
    -- Filter by hotness >= {min_hotness} and listens < {max_listens}
    SELECT 
        'PLACEHOLDER' as track_name,
        'PLACEHOLDER' as artist_name,
        0.0 as song_hotttnesss,
        0 as listens
    LIMIT 1;
    """
    return query


# ============================================
# LABEL ANALYSIS PAGE QUERIES
# ============================================

# TODO: TEAMMATE 3 - Label Success Query
def get_label_success_data():
    """
    PLACEHOLDER for Label Success bar chart
    Query should show top labels by total listens/tracks

    Expected columns:
    - label_name
    - total_tracks
    - total_listens
    - artist_count
    """
    query = """
    -- TODO: TEAMMATE 3 - Implement this query
    -- Hint: Join analytics.dim_labels with bridge_artist_labels
    -- Aggregate by label
    SELECT 
        'PLACEHOLDER' as label_name,
        0 as total_tracks,
        0 as total_listens
    LIMIT 1;
    """
    return query


# TODO: TEAMMATE 4 - Genre Trends Query
def get_genre_trends_heatmap():
    """
    PLACEHOLDER for Genre Trends heatmap
    Query should show genre popularity over time

    Expected columns:
    - year
    - genre_name
    - track_count OR popularity_metric
    """
    query = """
    -- TODO: TEAMMATE 4 - Implement this query
    -- Hint: Extract year from track_date_recorded
    -- Count tracks per genre per year
    SELECT 
        'PLACEHOLDER' as year,
        'PLACEHOLDER' as genre_name,
        0 as track_count
    LIMIT 1;
    """
    return query


# ============================================
# TRACK PERFORMANCE PAGE QUERIES
# ============================================

# TODO: TEAMMATE 5 - Track Performance Table Query
def get_track_performance_table(genre_filter: str = None, year_filter: int = None):
    """
    PLACEHOLDER for Track Performance sortable table
    Query should show detailed track metrics

    Expected columns:
    - track_name
    - artist_name
    - genre
    - listens
    - favorites
    - audio features
    """
    query = """
    -- TODO: TEAMMATE 5 - Implement this query
    -- Hint: Use analytics.fact_track_performance
    -- Join with dimensions for track/artist names
    SELECT 
        'PLACEHOLDER' as track_name,
        'PLACEHOLDER' as artist_name,
        0 as listens
    LIMIT 1;
    """
    return query


# TODO: TEAMMATE 6 - Feature Correlation Query
def get_feature_correlation_data():
    """
    PLACEHOLDER for Audio Features Correlation Matrix
    Query should fetch audio features for correlation calculation

    Expected columns:
    - All audio feature columns (energy, danceability, valence, etc.)
    """
    query = """
    -- TODO: TEAMMATE 6 - Implement this query
    -- Hint: SELECT all audio features from analytics.fact_track_performance
    -- or from public."Audio" table
    SELECT 
        energy, danceability, valence, acousticness,
        instrumentalness, liveness, speechiness
    FROM analytics.fact_track_performance
    WHERE energy IS NOT NULL
    LIMIT 1000;
    """
    return query


# ============================================
# UTILITY QUERIES
# ============================================

def get_year_range():
    """
    Get the min and max years in the dataset for date sliders
    """
    query = """
    SELECT 
        MIN(artist_active_year_begin) as min_year,
        MAX(artist_active_year_begin) as max_year
    FROM analytics.dim_artists
    WHERE artist_active_year_begin IS NOT NULL;
    """
    return query


def get_database_stats():
    """
    Get overall database statistics for dashboard
    """
    query = """
    SELECT 
        (SELECT COUNT(*) FROM analytics.dim_artists) as total_artists,
        (SELECT COUNT(*) FROM analytics.dim_genres) as total_genres,
        (SELECT COUNT(*) FROM analytics.fact_track_performance) as total_tracks,
        (SELECT COUNT(DISTINCT label_id) FROM analytics.bridge_artist_labels) as total_labels;
    """
    return query
