import ast
import os

import pandas as pd

RAW_DATA_DIR = 'fma_metadata'
CLEANED_DATA_DIR = 'fma_metadata_cleaned'

# These are the columns we actually need from each raw CSV file
COLUMNS_TO_KEEP = {
    'genres': ['genre_id', 'genre_parent_id', 'genre_title'],
    'artists': ['artist_id', 'artist_active_year_begin', 'artist_associated_labels', 'artist_contact',
                'artist_favorites', 'artist_handle', 'artist_members', 'artist_name', 'artist_website',
                'artist_latitude', 'artist_longitude', 'artist_location'],
    'albums': ['album_id', 'album_date_released', 'album_engineer', 'album_favorites', 'album_listens',
               'album_producer', 'album_title', 'album_tracks', 'album_type', 'artist_name', 'album_url'],
    'tracks': ['track_id', 'album_id', 'artist_id', 'license_title', 'license_url', 'track_bit_rate', 'track_composer',
               'track_date_recorded', 'track_duration', 'track_favorites', 'track_genres', 'track_language_code',
               'track_listens', 'track_lyricist', 'track_title', 'track_url'],
    'echonest': ['Unnamed: 0', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness',
                 'tempo', 'valence', 'artist_discovery', 'artist_familiarity', 'artist_hotttnesss', 'song_currency',
                 'song_hotttnesss']
}


def load_raw_data():
    """
    Load the original raw CSV files from the fma_metadata folder.
    Only load the columns we actually need to save memory.
    """
    print("\nLoading raw data files...")
    print(f"Looking in: {os.path.join(os.getcwd(), RAW_DATA_DIR)}\n")

    raw_data = {}

    try:
        for file_name, columns in COLUMNS_TO_KEEP.items():
            file_path = os.path.join(RAW_DATA_DIR, f"raw_{file_name}.csv")

            # The echonest file has a weird structure with headers on row 3 instead of row 1
            header_row = 2 if file_name == 'echonest' else 0

            raw_data[file_name] = pd.read_csv(file_path, usecols=columns, header=header_row, low_memory=False)
            print(f"Loaded {file_name}: {len(raw_data[file_name]):,} rows")

        return raw_data

    except FileNotFoundError as e:
        print(f"\nERROR: Could not find data files")
        print(f"Make sure your raw CSV files are in the '{RAW_DATA_DIR}' folder")
        print(f"Details: {e}")
        return None


def clean_genres(raw_genres):
    """
    Clean the genres data and fix any orphaned parent references.
    Some genres reference parent genres that don't exist in the dataset.
    """
    genres = raw_genres.copy()
    genres.columns = genres.columns.str.lower()
    genres.dropna(subset=['genre_id'], inplace=True)
    genres = genres.astype({'genre_id': int})

    # Fix any genres that point to non-existent parents
    existing_ids = set(genres['genre_id'].values)
    has_parent = genres['genre_parent_id'].notna()
    parent_missing = ~genres['genre_parent_id'].isin(existing_ids)
    orphaned_genres = has_parent & parent_missing

    orphan_count = orphaned_genres.sum()
    if orphan_count > 0:
        print(f"  Found {orphan_count} genres with invalid parent references")
        print(f"  Converting them to top-level genres")
        genres.loc[orphaned_genres, 'genre_parent_id'] = pd.NA

    return genres


def clean_artists(raw_artists):
    """Clean the artists data."""
    artists = raw_artists.copy()
    artists.columns = artists.columns.str.lower()
    artists.dropna(subset=['artist_id'], inplace=True)
    artists = artists.astype({'artist_id': int})
    return artists


def clean_albums(raw_albums, clean_artists):
    """
    Clean the albums data.
    Remove any albums that reference artists that don't exist in our cleaned data.
    """
    albums = raw_albums.copy()
    albums.columns = albums.columns.str.lower()
    albums.dropna(subset=['album_id', 'artist_name'], inplace=True)
    albums['album_id'] = albums['album_id'].astype(int)

    # Only keep albums for artists we have in our database
    valid_artists = set(clean_artists['artist_name'])
    before_count = len(albums)
    albums = albums[albums['artist_name'].isin(valid_artists)]
    after_count = len(albums)

    removed = before_count - after_count
    if removed > 0:
        print(f"  Removed {removed:,} albums with unknown artists")

    return albums


def clean_tracks(raw_tracks, clean_albums, clean_artists):
    """
    Clean the tracks data.
    Remove any tracks that reference albums or artists that don't exist.
    """
    tracks = raw_tracks.copy()
    tracks.columns = tracks.columns.str.lower()
    tracks.dropna(subset=['track_id', 'track_title'], inplace=True)
    tracks['track_id'] = tracks['track_id'].astype(int)

    # Only keep tracks that link to valid albums and artists
    valid_albums = set(clean_albums['album_id'])
    valid_artists = set(clean_artists['artist_id'])

    before_count = len(tracks)
    tracks = tracks[
        tracks['album_id'].isin(valid_albums) &
        tracks['artist_id'].isin(valid_artists)
        ]
    after_count = len(tracks)

    removed = before_count - after_count
    if removed > 0:
        print(f"  Removed {removed:,} tracks with invalid album/artist references")

    return tracks


def clean_echonest(raw_echonest):
    """
    Clean the echonest features data.
    This file has audio and social features for tracks.
    """
    echonest = raw_echonest.copy()
    echonest.columns = echonest.columns.str.lower()
    echonest.rename(columns={'unnamed: 0': 'track_id'}, inplace=True)

    # Remove any rows where track_id isn't a valid number
    echonest = echonest[pd.to_numeric(echonest['track_id'], errors='coerce').notna()]
    echonest['track_id'] = echonest['track_id'].astype(int)

    return echonest


def save_cleaned_data(clean_data):
    """Save all the cleaned data to new CSV files."""
    os.makedirs(CLEANED_DATA_DIR, exist_ok=True)

    print(f"\nSaving cleaned files to: {CLEANED_DATA_DIR}/")

    for name, data in clean_data.items():
        output_file = os.path.join(CLEANED_DATA_DIR, f"clean_{name}.csv")
        data.to_csv(output_file, index=False)
        print(f"  Saved clean_{name}.csv ({len(data):,} rows)")


def analyze_column_coverage(df, column_name, entity_name):
    """
    Check how much data exists in a column and whether it's worth creating a table for it.
    """
    rows_with_data = df[column_name].dropna()
    total_rows = len(df)
    coverage_percent = (len(rows_with_data) / total_rows * 100) if total_rows > 0 else 0

    # Count unique values (split by common delimiters like commas and ampersands)
    unique_values = (rows_with_data
                     .astype(str)
                     .str.split(r'[,&\n]')
                     .explode()
                     .str.strip()
                     .nunique())

    print(f"\n{entity_name}:")
    print(f"  Coverage: {len(rows_with_data):,} out of {total_rows:,} rows ({coverage_percent:.1f}%)")
    print(f"  Unique values: {unique_values:,}")

    if coverage_percent > 5:
        print(f"  ✓ Good coverage - worth creating a table")
    else:
        print(f"  ✗ Very low coverage - table would be mostly empty")


def analyze_genre_links(tracks_df, genres_df):
    """
    Check how many valid track-to-genre links we have.
    Genre data is stored as a complex nested structure in the CSV.
    """
    valid_genre_ids = set(genres_df['genre_id'])
    valid_links = 0

    for genre_string in tracks_df['track_genres'].dropna():
        try:
            # Parse the genre data (it's stored as a string representation of a list)
            genres_list = ast.literal_eval(genre_string)
            for genre in genres_list:
                genre_id = int(genre.get('genre_id'))
                if genre_id in valid_genre_ids:
                    valid_links += 1
        except (ValueError, SyntaxError):
            continue

    print(f"\nTrack-Genre Links:")
    print(f"  Valid links: {valid_links:,}")
    print(f"  ✓ TrackGenres linking table is essential for this relationship")


def run_analysis(clean_data):
    """
    Analyze the cleaned data to see what tables are worth creating.
    This helps us decide if certain normalized tables will have enough data.
    """
    print("\n" + "=" * 80)
    print("DATA ANALYSIS - Checking coverage for potential tables")
    print("=" * 80)

    # Check if each entity has enough data to justify a separate table
    analyze_column_coverage(clean_data['albums'], 'album_engineer', 'Engineers')
    analyze_column_coverage(clean_data['tracks'], 'track_lyricist', 'Lyricists')
    analyze_column_coverage(clean_data['artists'], 'artist_associated_labels', 'Labels')
    analyze_column_coverage(clean_data['tracks'], 'license_title', 'Licenses')

    # Check the genre linking situation
    analyze_genre_links(clean_data['tracks'], clean_data['genres'])


def main():
    """Run the complete data cleaning pipeline."""

    print("=" * 80)
    print("FMA DATA CLEANING PIPELINE")
    print("=" * 80)

    # Step 1: Load the raw data
    raw_data = load_raw_data()
    if not raw_data:
        return

    # Step 2: Clean each file
    # We clean in order: independent tables first, then dependent tables
    print("\n" + "=" * 80)
    print("CLEANING DATA")
    print("=" * 80)

    print("\nCleaning independent tables...")
    clean_data = {}
    clean_data['genres'] = clean_genres(raw_data['genres'])
    clean_data['artists'] = clean_artists(raw_data['artists'])

    print("\nCleaning dependent tables...")
    clean_data['albums'] = clean_albums(raw_data['albums'], clean_data['artists'])
    clean_data['tracks'] = clean_tracks(raw_data['tracks'], clean_data['albums'], clean_data['artists'])
    clean_data['echonest'] = clean_echonest(raw_data['echonest'])

    # Step 3: Save the cleaned data
    save_cleaned_data(clean_data)

    # Step 4: Run analysis on the cleaned data
    run_analysis(clean_data)

    print("\n" + "=" * 80)
    print("✓ CLEANING COMPLETE")
    print("=" * 80)
    print(f"\nCleaned files are ready in the '{CLEANED_DATA_DIR}' folder")
    print("You can now run the ingestion script to load data into the database")


if __name__ == "__main__":
    main()
