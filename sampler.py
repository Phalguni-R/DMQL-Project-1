import pandas as pd
import os

# =================================================================================
# --- CONFIGURATION ---
# =================================================================================
# This script creates a small, sampled version of the large raw dataset.
# This is useful for faster testing and development.

# The folder containing your original large CSV files.
SOURCE_DIR = 'fma_metadata'

# The folder where the new, smaller CSV files will be saved.
OUTPUT_DIR = 'fma_metadata_sampled'

# The number of rows you want in your sample files.
ROWS_TO_SAMPLE = 3000

# --- Automatically build full paths ---
CWD = os.getcwd()
SOURCE_PATH = os.path.join(CWD, SOURCE_DIR)
OUTPUT_PATH = os.path.join(CWD, OUTPUT_DIR)


def main():
    """
    Main function to sample all CSVs in the source directory.
    """
    # Check if the source directory exists
    if not os.path.isdir(SOURCE_PATH):
        print(f"Error: Source directory '{SOURCE_PATH}' not found.")
        return

    # Create the output directory if it doesn't exist
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    print(f"Output will be saved to: '{OUTPUT_PATH}'")

    # Loop through each file in the source directory
    for filename in os.listdir(SOURCE_PATH):
        if filename.endswith('.csv'):
            source_file = os.path.join(SOURCE_PATH, filename)
            output_file = os.path.join(OUTPUT_PATH, filename)

            try:
                print(f"Processing '{filename}'...")

                # Some files have multi-level headers, so we handle that.
                header_row = 2 if 'echonest' in filename else 0

                # Read only the first 'rows_to_sample' rows from the CSV
                df = pd.read_csv(source_file, header=header_row, nrows=ROWS_TO_SAMPLE, low_memory=False)

                # Save the sampled dataframe to a new CSV file
                df.to_csv(output_file, index=False)
                print(f"  -> Successfully created sample with {len(df)} rows.")

            except Exception as e:
                print(f"  -> Could not process {filename}. Error: {e}")

    print("\nScript finished.")


if __name__ == "__main__":
    main()
