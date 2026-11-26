
import pandas as pd
from pathlib import Path

# Find CSV files
files = list(Path("data/raw").glob("*.csv"))

# Check if a CSV file exists
if not files:
    raise FileNotFoundError("No CSV file found")

# Read the dataset
df = pd.read_csv(files[0], low_memory=False)

# Display dataset dimensions
print("Rows and columns:", df.shape)

# Display column names
print("\nColumn names:")
print(df.columns.tolist())

# Display first 10 records
print("\nFirst 10 rows:")
print(df.head(10).to_string())

# Check missing values
print("\nMissing values:")
print(df.isnull().sum())
