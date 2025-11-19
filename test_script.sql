
-- Analyst User

-- TEST 1: SELECT should work
SELECT COUNT(*) as total_artists FROM "Artists";

-- TEST 2: GET 5 rows from Artists
SELECT artist_name, artist_favorites
FROM "Artists"
LIMIT 5;

-- TEST 3: DELETE should FAIL
DELETE FROM "Artists" WHERE artist_id = 1;


-- Developer User

-- TEST 1: SELECT should work
SELECT COUNT(*) as total_tracks FROM "Tracks";

SELECT track_title, track_listens
FROM "Tracks"
LIMIT 5;

-- TEST 2: INSERT should work
INSERT INTO "Artists" (artist_id, artist_name, artist_handle)
VALUES (999999, 'Test Artist', 'test_handle');

-- TEST 3: View the Inserted data
SELECT *
FROM "Artists"
WHERE artist_id=999999;

-- TEST 4: UPDATE should work
UPDATE "Artists"
SET artist_favorites = 100
WHERE artist_id = 999999;

-- TEST 5: Vew the Updated data
SELECT *
FROM "Artists"
WHERE artist_id=999999;

-- TEST 6: DELETE should work
DELETE FROM "Artists" WHERE artist_id = 999999;

-- TEST 7: View the Deleted data -> should be empty
SELECT *
FROM "Artists"
WHERE artist_id=999999;
