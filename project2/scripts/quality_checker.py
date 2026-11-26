
import pandas as pd
from pathlib import Path

# Project directories
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
TEST_DIR = BASE_DIR / "tests"
REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

REQUIRED_COLUMNS = [
    "purchase_id",
    "date",
    "supplier",
    "item",
    "quantity",
    "unit_price",
    "total"
]

ERROR_COLUMNS = [
    "file",
    "row_number",
    "column",
    "error_type"
]


# Main validation function
def check_quality(file_path):

    df = pd.read_csv(file_path, dtype=str)

    errors = []

    def add_error(index, column, error_type):
        errors.append({
            "file": file_path.name,
            "row_number": index + 2,
            "column": column,
            "error_type": error_type
        })

    # Check required columns
    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    # RULE 1: Missing values
    for column in REQUIRED_COLUMNS:

        missing = (
            df[column].isna() |
            df[column].fillna("").str.strip().eq("")
        )

        for index in df.index[missing]:
            add_error(index, column, "Missing value")

    # RULE 2: Invalid numeric values
    numeric_columns = [
        "quantity",
        "unit_price",
        "total"
    ]

    numbers = {}

    for column in numeric_columns:

        converted = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        numbers[column] = converted

        invalid = (
            df[column].notna() &
            df[column].fillna("").str.strip().ne("") &
            (
                converted.isna() |
                converted.isin(
                    [float("inf"), float("-inf")]
                )
            )
        )

        for index in df.index[invalid]:
            add_error(index, column, "Invalid number")

        numbers[column] = converted.replace(
            [float("inf"), float("-inf")],
            float("nan")
        )

    # RULE 3: Negative prices
    negative = numbers["unit_price"] < 0

    for index in df.index[negative]:
        add_error(
            index, "unit_price", "Negative price"
        )

    # RULE 4: Zero prices
    zero = numbers["unit_price"] == 0

    for index in df.index[zero]:
        add_error(
            index, "unit_price", "Zero price"
        )

    # RULE 5: Incorrect total calculations
    expected_total = (
        numbers["quantity"] *
        numbers["unit_price"]
    ).round(2)

    difference = (
        expected_total - numbers["total"]
    ).abs().round(8)

    incorrect = difference > 0.01

    for index in df.index[incorrect]:
        add_error(index, "total", "Incorrect total")

    # RULE 6: Duplicate rows
    duplicates = df.duplicated(keep="first")

    for index in df.index[duplicates]:
        add_error(
            index, "All columns", "Duplicate row"
        )

    # RULE 7: Invalid dates
    dates = pd.to_datetime(
        df["date"],
        format="%Y-%m-%d",
        errors="coerce"
    )

    correct_format = df["date"].str.fullmatch(
        r"\d{4}-\d{2}-\d{2}",
        na=False
    )

    invalid_dates = (
        df["date"].notna() &
        df["date"].fillna("").str.strip().ne("") &
        (dates.isna() | ~correct_format)
    )

    for index in df.index[invalid_dates]:
        add_error(index, "date", "Invalid date")

    # RULE 8: Future dates
    today = pd.Timestamp.today().normalize()

    future_dates = (
        (dates > today) & correct_format
    )

    for index in df.index[future_dates]:
        add_error(index, "date", "Future date")

    return pd.DataFrame(
        errors,
        columns=ERROR_COLUMNS
    )


# Run checker on all datasets
if __name__ == "__main__":

    files = [
        DATA_DIR / "clean_purchases.csv"
    ]

    files += sorted(
        TEST_DIR.glob("test_*.csv")
    )

    all_errors = []

    print("=" * 50)
    print("AUTOMATED DATA QUALITY CHECKER")
    print("=" * 50)

    for file in files:

        results = check_quality(file)

        print(f"\nFile: {file.name}")
        print(f"Errors detected: {len(results)}")

        if results.empty:
            print("PASS: No quality issues found.")

        else:
            print(
                results["error_type"].value_counts()
            )

        all_errors.append(results)

    # Combine detected errors
    final_results = pd.concat(
        all_errors,
        ignore_index=True
    )

    output_path = (
        REPORT_DIR / "detected_errors.csv"
    )

    final_results.to_csv(
        output_path,
        index=False
    )

    print("\n" + "=" * 50)
    print(
        "Total errors detected:",
        len(final_results)
    )
    print("Report saved:", output_path)
    print("=" * 50)
