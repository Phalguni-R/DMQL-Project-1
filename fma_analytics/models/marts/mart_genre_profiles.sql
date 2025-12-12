SELECT
    g.genre_name,
    COUNT(DISTINCT t.track_id) as track_count,
    AVG(a.danceability) as avg_danceability,
    AVG(a.energy) as avg_energy,
    AVG(a.acousticness) as avg_acousticness,
    AVG(a.instrumentalness) as avg_instrumentalness,
    AVG(a.liveness) as avg_liveness,
    AVG(a.speechiness) as avg_speechiness,
    AVG(a.valence) as avg_valence
FROM {{ source('public', 'Genres') }} g
JOIN {{ source('public', 'TrackGenres') }} tg ON g.genre_id = tg.genre_id
JOIN {{ source('public', 'Tracks') }} t ON tg.track_id = t.track_id
LEFT JOIN {{ source('public', 'Audio') }} a ON t.track_id = a.track_id
GROUP BY g.genre_name
HAVING COUNT(DISTINCT t.track_id) > 0