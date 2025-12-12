{{ config(materialized='table') }}

SELECT
    artist_id,
    artist_name,
    artist_handle,
    artist_website,
    artist_active_year_begin,
    artist_favorites,
    artist_latitude,
    artist_longitude,
    artist_location
FROM {{ source('public', 'Artists') }}