-- 1. Genre Profiles
-- Shows audio fingerprint for each genre (genres with 100+ tracks)
SELECT
    genre_name,
    track_count,
    COALESCE(ROUND(avg_danceability::numeric, 3), 0) AS avg_danceability,
    COALESCE(ROUND(avg_energy::numeric, 3), 0) AS avg_energy
FROM analytics.mart_genre_profiles
ORDER BY avg_energy DESC;


-- 2. Top Artists Yearly
-- Shows top 3 artists per year by total listens
SELECT
    artist_name,
    release_year,
    total_listens,
    rank_in_year
FROM analytics.mart_top_artists_yearly
WHERE rank_in_year <= 3
  AND release_year > 2000
ORDER BY release_year DESC, rank_in_year ASC;


-- 3. Undiscovered Gems
-- High hotttnesss but below-average listens (hidden gems)
SELECT
    track_id,
    artist_name,
    track_listens,
    ROUND(song_hotttnesss::numeric, 3) AS song_hotttnesss
FROM analytics.mart_undiscovered_gems
ORDER BY song_hotttnesss DESC
LIMIT 50;


-- 4. Artist Profiles
-- Gives us artist profiles (top 100)
SELECT
    artist_id,
    artist_name,
    artist_active_year_begin,
    artist_favorites,
    album_count,
    track_count,
    total_listens,
    total_track_favorites,
    top_genre,
    associated_labels
FROM analytics.mart_artist_profiles
ORDER BY total_listens DESC, artist_favorites DESC
LIMIT 100;