
import re
import unicodedata
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)


def clean_header(header):
    """
    Normalize a column header for text matching.
    """

    # Convert to string
    header = str(header)

    # Normalize Unicode characters
    header = unicodedata.normalize("NFKC", header)

    # Convert to lowercase
    header = header.lower()

    # Replace underscores with spaces
    header = header.replace("_", " ")

    # Remove special characters
    header = re.sub(r"[^a-z0-9\s]", " ", header)

    # Remove extra spaces
    header = re.sub(r"\s+", " ", header)

    # Remove leading and trailing spaces
    header = header.strip()

    return header


def process_all_headers():

    results = []

    csv_files = sorted(
        DATA_DIR.glob("procurement_*.csv")
    )

    for file in csv_files:

        # Read only column headers
        df = pd.read_csv(file, nrows=0)

        for header in df.columns:

            cleaned = clean_header(header)

            results.append({
                "file_name": file.name,
                "original_header": header,
                "cleaned_header": cleaned
            })

    result_df = pd.DataFrame(results)

    output_file = REPORT_DIR / "cleaned_headers.csv"

    result_df.to_csv(output_file, index=False)

    print("=" * 50)
    print("HEADER NORMALIZATION COMPLETED")
    print("=" * 50)

    print(f"Files processed: {len(csv_files)}")
    print(f"Headers processed: {len(result_df)}")

    print("\nSample cleaned headers:")
    print(result_df.head(15).to_string(index=False))

    print(f"\nReport saved to: {output_file}")


if __name__ == "__main__":

    process_all_headers()

