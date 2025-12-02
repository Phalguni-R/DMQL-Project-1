-- Indexes to speed up joins and filtering
CREATE INDEX IF NOT EXISTS idx_trackgenres_genre_id ON public."TrackGenres"(genre_id);
CREATE INDEX IF NOT EXISTS idx_trackgenres_track_id ON public."TrackGenres"(track_id);
CREATE INDEX IF NOT EXISTS idx_audio_track_id ON public."Audio"(track_id);
CREATE INDEX IF NOT EXISTS idx_tracks_date_recorded ON public."Tracks"(track_date_recorded);
CREATE INDEX IF NOT EXISTS idx_tracks_artist_id ON public."Tracks"(artist_id);
CREATE INDEX IF NOT EXISTS idx_social_hotttnesss ON public."Social"(song_hotttnesss);
CREATE INDEX IF EXISTS idx_social_track_id ON public."Social"(track_id);
CREATE INDEX IF NOT EXISTS idx_artistlabels_label_id ON public."ArtistLabels"(label_id);
CREATE INDEX IF NOT EXISTS idx_artistlabels_artist_id ON public."ArtistLabels"(artist_id);
CREATE INDEX IF NOT EXISTS idx_albums_artist_id ON public."Albums"(artist_id);

-- Update stats so the planner sees the new indexes
ANALYZE;


-- OPTIONAL: DROP INDEXES (for before and after comparison)

-- DROP INDEX IF EXISTS public.idx_trackgenres_genre_id;
-- DROP INDEX IF EXISTS public.idx_trackgenres_track_id;
-- DROP INDEX IF EXISTS public.idx_audio_track_id;
-- DROP INDEX IF EXISTS public.idx_tracks_date_recorded;
-- DROP INDEX IF EXISTS public.idx_tracks_artist_id;
-- DROP INDEX IF EXISTS public.idx_social_hotttnesss;
-- DROP INDEX IF EXISTS public.idx_social_track_id;
-- DROP INDEX IF EXISTS public.idx_artistlabels_label_id;
-- DROP INDEX IF EXISTS public.idx_artistlabels_artist_id;
-- DROP INDEX IF EXISTS public.idx_albums_artist_id;