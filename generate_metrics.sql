-- Turn on timing to see total execution time
\timing on

\echo '----------------------------------------------------------------------'
\echo '>>> PREPARING ENVIRONMENT: DROPPING INDEXES...'
\echo '----------------------------------------------------------------------'

DROP INDEX IF EXISTS public.idx_trackgenres_genre_id;
DROP INDEX IF EXISTS public.idx_trackgenres_track_id;
DROP INDEX IF EXISTS public.idx_audio_track_id;
DROP INDEX IF EXISTS public.idx_tracks_date_recorded;
DROP INDEX IF EXISTS public.idx_tracks_artist_id;
DROP INDEX IF EXISTS public.idx_social_hotttnesss;
DROP INDEX IF EXISTS public.idx_social_track_id;
DROP INDEX IF EXISTS public.idx_artistlabels_label_id;
DROP INDEX IF EXISTS public.idx_artistlabels_artist_id;
DROP INDEX IF EXISTS public.idx_albums_artist_id;

-- Clear internal cache
DISCARD ALL;

-- PHASE 1: BEFORE INDEXING (RAW TABLES)
\echo ' '
\echo '>>> PHASE 1: BENCHMARKING RAW TABLES (NO INDEXES)'

\echo '-- Q1: Genre Fingerprinting (Raw) --'
EXPLAIN (ANALYZE, BUFFERS)
SELECT
    g.genre_name,
    COUNT(t.track_id) AS track_count,
    ROUND(AVG(a.danceability)::numeric, 3) AS avg_danceability,
    ROUND(AVG(a.energy)::numeric, 3) AS avg_energy
FROM public."Tracks" t
JOIN public."TrackGenres" tg ON t.track_id = tg.track_id
JOIN public."Genres" g ON tg.genre_id = g.genre_id
JOIN public."Audio" a ON t.track_id = a.track_id
GROUP BY g.genre_name
HAVING COUNT(t.track_id) > 100
ORDER BY avg_energy DESC;

\echo '-- Q2: Top Artists Yearly (Raw) --'
EXPLAIN (ANALYZE, BUFFERS)
WITH YearlyStats AS (
    SELECT
        art.artist_name,
        EXTRACT(YEAR FROM t.track_date_recorded) AS release_year,
        SUM(t.track_listens) AS total_listens
    FROM public."Tracks" t
    JOIN public."Artists" art ON t.artist_id = art.artist_id
    WHERE t.track_date_recorded > '2000-01-01'
    GROUP BY 1, 2
),
RankedStats AS (
    SELECT *, RANK() OVER (PARTITION BY release_year ORDER BY total_listens DESC) as yr_rank
    FROM YearlyStats
)
SELECT * FROM RankedStats
WHERE yr_rank <= 3
ORDER BY release_year DESC, yr_rank ASC;

\echo '-- Q3: Undiscovered Gems (Raw) --'
EXPLAIN (ANALYZE, BUFFERS)
SELECT
    t.track_title,
    art.artist_name,
    t.track_listens,
    s.song_hotttnesss
FROM public."Tracks" t
JOIN public."Social" s ON t.track_id = s.track_id
JOIN public."Artists" art ON t.artist_id = art.artist_id
WHERE s.song_hotttnesss > 0.6
  AND t.track_listens < (SELECT AVG(track_listens) FROM public."Tracks")
ORDER BY s.song_hotttnesss DESC
LIMIT 50;

\echo '-- Q4: Artist Profiling (Raw) --'
EXPLAIN (ANALYZE, BUFFERS)
SELECT
    a.artist_id,
    a.artist_name,
    a.artist_active_year_begin,
    a.artist_favorites,
    COUNT(DISTINCT al.album_id) as album_count,
    COUNT(DISTINCT t.track_id) as track_count,
    COALESCE(SUM(t.track_listens), 0) as total_listens,
    COALESCE(SUM(t.track_favorites), 0) as total_track_favorites,
    STRING_AGG(DISTINCT l.label_name, ', ') as associated_labels,
    (
        SELECT g.genre_name
        FROM public."TrackGenres" tg
        JOIN public."Genres" g ON tg.genre_id = g.genre_id
        JOIN public."Tracks" t2 ON tg.track_id = t2.track_id
        WHERE t2.artist_id = a.artist_id
        GROUP BY g.genre_name
        ORDER BY COUNT(*) DESC
        LIMIT 1
    ) as top_genre
FROM public."Artists" a
LEFT JOIN public."Albums" al ON a.artist_id = al.artist_id
LEFT JOIN public."Tracks" t ON a.artist_id = t.artist_id
LEFT JOIN public."Social" s ON t.track_id = s.track_id
LEFT JOIN public."ArtistLabels" arl ON a.artist_id = arl.artist_id
LEFT JOIN public."Labels" l ON arl.label_id = l.label_id
GROUP BY a.artist_id, a.artist_name, a.artist_active_year_begin, a.artist_favorites
ORDER BY total_listens DESC, artist_favorites DESC
LIMIT 10;


-- PHASE 2: APPLYING OPTIMIZATIONS
\echo ' '
\echo '>>> PHASE 2: APPLYING INDEXES...'

CREATE INDEX idx_trackgenres_genre_id ON public."TrackGenres"(genre_id);
CREATE INDEX idx_trackgenres_track_id ON public."TrackGenres"(track_id);
CREATE INDEX idx_audio_track_id ON public."Audio"(track_id);
CREATE INDEX idx_tracks_date_recorded ON public."Tracks"(track_date_recorded);
CREATE INDEX idx_tracks_artist_id ON public."Tracks"(artist_id);
CREATE INDEX idx_social_hotttnesss ON public."Social"(song_hotttnesss);
CREATE INDEX idx_social_track_id ON public."Social"(track_id);
CREATE INDEX idx_artistlabels_label_id ON public."ArtistLabels"(label_id);
CREATE INDEX idx_artistlabels_artist_id ON public."ArtistLabels"(artist_id);
CREATE INDEX idx_albums_artist_id ON public."Albums"(artist_id);

-- Update statistics
ANALYZE;
DISCARD ALL;


-- PHASE 3: AFTER INDEXING (OPTIMIZED)
\echo ' '
\echo '>>> PHASE 3: BENCHMARKING OPTIMIZED TABLES (WITH INDEXES)'

\echo '-- Q1: Genre Fingerprinting (Optimized) --'
EXPLAIN (ANALYZE, BUFFERS)
SELECT
    g.genre_name,
    COUNT(t.track_id) AS track_count,
    ROUND(AVG(a.danceability)::numeric, 3) AS avg_danceability,
    ROUND(AVG(a.energy)::numeric, 3) AS avg_energy
FROM public."Tracks" t
JOIN public."TrackGenres" tg ON t.track_id = tg.track_id
JOIN public."Genres" g ON tg.genre_id = g.genre_id
JOIN public."Audio" a ON t.track_id = a.track_id
GROUP BY g.genre_name
HAVING COUNT(t.track_id) > 100
ORDER BY avg_energy DESC;

\echo '-- Q2: Top Artists Yearly (Optimized) --'
EXPLAIN (ANALYZE, BUFFERS)
WITH YearlyStats AS (
    SELECT
        art.artist_name,
        EXTRACT(YEAR FROM t.track_date_recorded) AS release_year,
        SUM(t.track_listens) AS total_listens
    FROM public."Tracks" t
    JOIN public."Artists" art ON t.artist_id = art.artist_id
    WHERE t.track_date_recorded > '2000-01-01'
    GROUP BY 1, 2
),
RankedStats AS (
    SELECT *, RANK() OVER (PARTITION BY release_year ORDER BY total_listens DESC) as yr_rank
    FROM YearlyStats
)
SELECT * FROM RankedStats
WHERE yr_rank <= 3
ORDER BY release_year DESC, yr_rank ASC;

\echo '-- Q3: Undiscovered Gems (Optimized) --'
EXPLAIN (ANALYZE, BUFFERS)
SELECT
    t.track_title,
    art.artist_name,
    t.track_listens,
    s.song_hotttnesss
FROM public."Tracks" t
JOIN public."Social" s ON t.track_id = s.track_id
JOIN public."Artists" art ON t.artist_id = art.artist_id
WHERE s.song_hotttnesss > 0.6
  AND t.track_listens < (SELECT AVG(track_listens) FROM public."Tracks")
ORDER BY s.song_hotttnesss DESC
LIMIT 50;

\echo '-- Q4: Artist Profiling (Optimized) --'
EXPLAIN (ANALYZE, BUFFERS)
SELECT
    a.artist_id,
    a.artist_name,
    a.artist_active_year_begin,
    a.artist_favorites,
    COUNT(DISTINCT al.album_id) as album_count,
    COUNT(DISTINCT t.track_id) as track_count,
    COALESCE(SUM(t.track_listens), 0) as total_listens,
    COALESCE(SUM(t.track_favorites), 0) as total_track_favorites,
    STRING_AGG(DISTINCT l.label_name, ', ') as associated_labels,
    (
        SELECT g.genre_name
        FROM public."TrackGenres" tg
        JOIN public."Genres" g ON tg.genre_id = g.genre_id
        JOIN public."Tracks" t2 ON tg.track_id = t2.track_id
        WHERE t2.artist_id = a.artist_id
        GROUP BY g.genre_name
        ORDER BY COUNT(*) DESC
        LIMIT 1
    ) as top_genre
FROM public."Artists" a
LEFT JOIN public."Albums" al ON a.artist_id = al.artist_id
LEFT JOIN public."Tracks" t ON a.artist_id = t.artist_id
LEFT JOIN public."Social" s ON t.track_id = s.track_id
LEFT JOIN public."ArtistLabels" arl ON a.artist_id = arl.artist_id
LEFT JOIN public."Labels" l ON arl.label_id = l.label_id
GROUP BY a.artist_id, a.artist_name, a.artist_active_year_begin, a.artist_favorites
ORDER BY total_listens DESC, artist_favorites DESC
LIMIT 10;


-- PHASE 4: DBT ANALYTICS TABLES
\echo ' '
\echo '>>> PHASE 4: BENCHMARKING DBT MATERIALIZED TABLES'
\echo '>>> (Reading from pre-calculated tables in "analytics" schema)'

\echo '-- Q1: Genre Fingerprinting (From DBT Mart) --'
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM analytics.mart_genre_profiles
ORDER BY avg_energy DESC;

\echo '-- Q2: Top Artists Yearly (From DBT Mart) --'
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM analytics.mart_top_artists_yearly
WHERE rank_in_year <= 3
ORDER BY release_year DESC, rank_in_year ASC;

\echo '-- Q3: Undiscovered Gems (From DBT Mart) --'
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM analytics.mart_undiscovered_gems
ORDER BY song_hotttnesss DESC
LIMIT 50;

\echo '-- Q4: Artist Profiling (From DBT Mart) --'
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM analytics.mart_artist_profiles
ORDER BY total_listens DESC
LIMIT 10;