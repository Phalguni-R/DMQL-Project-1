def get_hidden_gems_data(min_hotness: float = 0.5, max_listens: int = 10000):
    """
    Query for Hidden Gems scatter plot
    Find high-quality tracks with low listen counts
    """
    query = f"""
    SELECT 
        t.track_title as track_name,
        ug.artist_name,
        ug.song_hotttnesss,
        ug.track_listens as listens,
        g.genre_name,
        au.energy,
        au.danceability,
        au.valence
    FROM analytics.mart_undiscovered_gems ug
    JOIN public."Tracks" t ON ug.track_id = t.track_id
    LEFT JOIN public."Audio" au ON ug.track_id = au.track_id
    LEFT JOIN public."TrackGenres" tg ON ug.track_id = tg.track_id
    LEFT JOIN public."Genres" g ON tg.genre_id = g.genre_id
    WHERE ug.song_hotttnesss >= {min_hotness}
      AND ug.track_listens <= {max_listens}
    ORDER BY ug.song_hotttnesss DESC
    LIMIT 500;
    """
    return query


def get_audio_features_correlation(genre_filter: str = None):
    """
    Query for Audio Features Correlation Matrix
    Get audio features for correlation analysis
    """
    if genre_filter and genre_filter != "All Genres":
        query = f"""
        SELECT 
            a.energy,
            a.danceability,
            a.valence,
            a.acousticness,
            a.instrumentalness,
            a.liveness,
            a.speechiness
        FROM public."Audio" a
        WHERE a.track_id IN (
            SELECT tg.track_id 
            FROM public."TrackGenres" tg
            JOIN public."Genres" g ON tg.genre_id = g.genre_id
            WHERE g.genre_name = '{genre_filter}'
        )
        AND a.energy IS NOT NULL
        AND a.danceability IS NOT NULL
        AND a.valence IS NOT NULL
        AND a.acousticness IS NOT NULL
        AND a.instrumentalness IS NOT NULL
        AND a.liveness IS NOT NULL
        AND a.speechiness IS NOT NULL
        LIMIT 5000;
        """
    else:
        query = """
        SELECT 
            a.energy,
            a.danceability,
            a.valence,
            a.acousticness,
            a.instrumentalness,
            a.liveness,
            a.speechiness
        FROM public."Audio" a
        WHERE a.energy IS NOT NULL
          AND a.danceability IS NOT NULL
          AND a.valence IS NOT NULL
          AND a.acousticness IS NOT NULL
          AND a.instrumentalness IS NOT NULL
          AND a.liveness IS NOT NULL
          AND a.speechiness IS NOT NULL
        LIMIT 5000;
        """

    return query


def get_available_genres_simple():
    """
    Get list of all available genres for dropdown filter
    """
    query = """
    SELECT DISTINCT genre_name
    FROM analytics.mart_genre_profiles
    WHERE track_count > 50
    ORDER BY genre_name;
    """
    return query

