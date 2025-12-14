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


