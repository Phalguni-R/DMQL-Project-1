"""
SQL Queries for Dashboard Visualizations
All queries use dbt analytics tables for optimal performance
"""


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

def get_top_genres_yearly(year_start: int = None, year_end: int = None):
    """ 
    Get ranked genres yearly
    """
    
    query = """
    WITH YearlyStats AS (
        SELECT
            g.genre_name,
            EXTRACT(YEAR FROM t.track_date_recorded) AS release_year,
            SUM(t.track_listens) AS total_listens
        FROM analytics.dim_genres g 
        JOIN analytics.bridge_track_genres tg ON tg.genre_id = g.genre_id
        JOIN analytics.fact_track_performance t ON tg.track_id = t.track_id 
        WHERE t.track_date_recorded > '1900-01-01'
        GROUP BY 1,2
    ),
    RankedStats AS (
        SELECT *, RANK() OVER (PARTITION BY release_year ORDER BY total_listens DESC) as yr_rank
        FROM YearlyStats
    )
    SELECT * FROM RankedStats
    WHERE yr_rank <= 10
    ORDER BY release_year DESC, yr_rank ASC;
    """

    return query