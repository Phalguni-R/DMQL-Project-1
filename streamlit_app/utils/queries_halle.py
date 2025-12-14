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

def get_top_artists_yearly(year_start: int = None, year_end: int = None):
    """ 
    Get ranked artist yearly
    """
    
    query = """
        SELECT
            prof.artist_id,
            prof.artist_name,
            top.release_year,
            top.total_listens,
            top.rank_in_year,
            prof.top_genre,
            prof.associated_labels
        FROM analytics.mart_top_artists_yearly top
        JOIN analytics.mart_artist_profiles prof on top.artist_name = prof.artist_name
        WHERE rank_in_year <= 10
        ORDER BY release_year DESC, rank_in_year ASC
    """
    
    return query


