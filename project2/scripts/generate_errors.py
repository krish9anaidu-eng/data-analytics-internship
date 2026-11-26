
import pandas as pd
from pathlib import Path

# Project directories
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
TEST_DIR = BASE_DIR / "tests"

TEST_DIR.mkdir(parents=True, exist_ok=True)

# Load clean dataset
clean = pd.read_csv(DATA_DIR / "clean_purchases.csv")

answer_key = []

# Function to record intentional errors
def record_error(filename, index, column, error_type):
    answer_key.append({
        "file": filename,
        "row_number": index + 2,
        "column": column,
        "error_type": error_type
    })


# TEST 1: Missing values
filename = "test_01_missing.csv"
df = clean.copy()

for i in range(10):
    df.loc[i, "supplier"] = None
    record_error(filename, i, "supplier", "Missing value")

df.to_csv(TEST_DIR / filename, index=False)


# TEST 2: Invalid prices
filename = "test_02_prices.csv"
df = clean.copy()

for i in range(10, 15):
    df.loc[i, "unit_price"] = -50
    df.loc[i, "total"] = df.loc[i, "quantity"] * -50
    record_error(filename, i, "unit_price", "Negative price")

for i in range(15, 20):
    df.loc[i, "unit_price"] = 0
    df.loc[i, "total"] = 0
    record_error(filename, i, "unit_price", "Zero price")

df.to_csv(TEST_DIR / filename, index=False)


# TEST 3: Incorrect totals
filename = "test_03_totals.csv"
df = clean.copy()

for i in range(20, 30):
    df.loc[i, "total"] += 100
    record_error(filename, i, "total", "Incorrect total")

df.to_csv(TEST_DIR / filename, index=False)


# TEST 4: Duplicate records
filename = "test_04_duplicates.csv"
df = clean.copy()

duplicates = df.iloc[30:40].copy()

df = pd.concat(
    [df, duplicates],
    ignore_index=True
)

for i in range(1000, 1010):
    record_error(filename, i, "All columns", "Duplicate row")

df.to_csv(TEST_DIR / filename, index=False)


# TEST 5: Mixed errors
filename = "test_05_mixed.csv"
df = clean.copy()

df["quantity"] = df["quantity"].astype(object)
df["unit_price"] = df["unit_price"].astype(object)

# Invalid dates
for i in range(40, 45):
    df.loc[i, "date"] = "2026-15-45"
    record_error(filename, i, "date", "Invalid date")

# Future dates
for i in range(45, 50):
    df.loc[i, "date"] = "2099-01-01"
    record_error(filename, i, "date", "Future date")

# Text in quantity
for i in range(50, 55):
    df.loc[i, "quantity"] = "ABC"
    record_error(filename, i, "quantity", "Invalid number")

# Text in unit price
for i in range(55, 60):
    df.loc[i, "unit_price"] = "INVALID"
    record_error(filename, i, "unit_price", "Invalid number")

df.to_csv(TEST_DIR / filename, index=False)


# Save answer key
answer_df = pd.DataFrame(answer_key)

answer_df.to_csv(
    TEST_DIR / "answer_key.csv",
    index=False
)

# Display summary
print("All test datasets generated successfully!")
print("\nTotal intentional errors:", len(answer_df))

print("\nErrors by file:")
print(answer_df.groupby("file").size())

print("\nErrors by type:")
print(answer_df["error_type"].value_counts())

print("\nFiles saved in:", TEST_DIR)

