
import pandas as pd
from pathlib import Path

# Load the CSV file
files = list(Path("data/raw").glob("*.csv"))

if len(files) != 1:
    raise ValueError("Keep one selected transaction CSV in data/raw.")

df = pd.read_csv(files[0], low_memory=False)

print("Original rows:", len(df))

# Clean column names
df.columns = df.columns.str.strip().str.lower()

# Remove duplicate rows
df = df.drop_duplicates()

# Convert dates
df["action_date"] = pd.to_datetime(
    df["action_date"], errors="coerce"
)

# Convert spending amounts to numbers
df["federal_action_obligation"] = pd.to_numeric(
    df["federal_action_obligation"], errors="coerce"
)

# Remove missing dates and amounts
df = df.dropna(subset=[
    "action_date",
    "federal_action_obligation"
])

# Handle missing supplier names
df["recipient_name"] = df["recipient_name"].fillna("Unknown")

# Create month column
df["month"] = df["action_date"].dt.strftime("%Y-%m")

# Save cleaned data
Path("data/cleaned").mkdir(parents=True, exist_ok=True)
df.to_csv("data/cleaned/cleaned_spend.csv", index=False)

print("Cleaned rows:", len(df))
print("Data cleaning completed successfully!")
