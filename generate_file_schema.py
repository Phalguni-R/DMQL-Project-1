import json
import os

import pandas as pd

# List of directories to scan for CSV files.
DIRECTORIES_TO_SCAN = [
    'fma_metadata',  # The raw data
    'fma_metadata_cleaned'  # The cleaned data
]

# The path where the final JSON file will be saved.
OUTPUT_JSON_PATH = 'files_schema.json'

# --- Automatically build full paths ---
CWD = os.getcwd()
OUTPUT_JSON_FULL_PATH = os.path.join(CWD, OUTPUT_JSON_PATH)


def get_directory_schema(directory_path, num_samples=3):
    """
    Reads all CSV files in a single directory and extracts their schema.
    """
    dir_schema = {}

    if not os.path.isdir(directory_path):
        print(f"Warning: Directory '{directory_path}' not found. Skipping.")
        return None

    print(f"\nScanning directory: '{directory_path}'...")
    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory_path, filename)
            try:
                # Read just the header to get all column names correctly.
                header_df = pd.read_csv(file_path, nrows=0, low_memory=False)
                # Read a few sample rows for the example.
                sample_df = pd.read_csv(file_path, nrows=num_samples, low_memory=False)

                dir_schema[filename] = {
                    'columns': header_df.columns.tolist(),
                    'example_rows': sample_df.to_dict(orient='records')
                }
                print(f"  - Processed '{filename}'")
            except Exception as e:
                print(f"  - Could not process file {filename}. Error: {e}")

    return dir_schema


def main():
    """
    Main function to generate and save the schema for all specified directories.
    """
    full_schema = {}

    for dir_name in DIRECTORIES_TO_SCAN:
        dir_full_path = os.path.join(CWD, dir_name)
        schema = get_directory_schema(dir_full_path)
        if schema:
            full_schema[dir_name] = schema

    if full_schema:
        try:
            with open(OUTPUT_JSON_FULL_PATH, 'w') as json_file:
                json.dump(full_schema, json_file, indent=4)
            print(f"\nSuccessfully created JSON schema at: '{OUTPUT_JSON_FULL_PATH}'")
        except Exception as e:
            print(f"\nError saving to JSON file: {e}")


if __name__ == '__main__':
    main()
