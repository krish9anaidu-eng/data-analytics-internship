
import pandas as pd
from pathlib import Path

# Project directories
BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"
TEST_DIR = BASE_DIR / "tests"
REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Load detected errors
errors = pd.read_csv(
    REPORT_DIR / "detected_errors.csv"
)

# Collect all datasets
files = [DATA_DIR / "clean_purchases.csv"]

files += sorted(TEST_DIR.glob("test_*.csv"))

summary = []

# Calculate quality scores
for file in files:

    df = pd.read_csv(file)

    total_rows = len(df)

    file_errors = errors[
        errors["file"] == file.name
    ]

    total_errors = len(file_errors)

    affected_rows = (
        file_errors["row_number"].nunique()
    )

    clean_rows = total_rows - affected_rows

    quality_score = (
        clean_rows / total_rows * 100
        if total_rows > 0 else 0
    )

    quality_score = round(quality_score, 2)

    # Assign quality status
    if total_rows == 0:
        status = "Empty Dataset"

    elif quality_score == 100:
        status = "Excellent"

    elif quality_score >= 95:
        status = "Good"

    elif quality_score >= 80:
        status = "Needs Improvement"

    else:
        status = "Poor"

    summary.append({
        "file": file.name,
        "total_rows": total_rows,
        "total_errors": total_errors,
        "affected_rows": affected_rows,
        "clean_rows": clean_rows,
        "quality_score": quality_score,
        "status": status
    })

# Create summary DataFrame
summary_df = pd.DataFrame(summary)

# Save report
output_path = REPORT_DIR / "quality_summary.csv"

summary_df.to_csv(output_path, index=False)

# Display results
print("=" * 70)
print("DATA QUALITY SCORE REPORT")
print("=" * 70)

print(summary_df.to_string(index=False))

print("\nReport saved:", output_path)
