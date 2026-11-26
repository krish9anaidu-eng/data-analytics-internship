
import pandas as pd
from faker import Faker
import random
from pathlib import Path

# Initialize Faker
fake = Faker()

Faker.seed(42)
random.seed(42)

# Output directory
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(parents=True, exist_ok=True)

# Generate 20 synthetic suppliers
suppliers = [
    fake.company() for _ in range(20)
]

# Procurement items
items = [
    "Laptop",
    "Office Chair",
    "Keyboard",
    "Monitor",
    "Safety Gloves",
    "Printer",
    "Cleaning Supplies",
    "Steel Bolts",
    "Safety Helmet",
    "USB Cable",
    "Office Desk",
    "Packaging Boxes",
    "Safety Shoes",
    "Mouse",
    "Industrial Tools"
]

# Generate 1,000 purchase records
records = []

for i in range(1, 1001):

    quantity = random.randint(1, 100)

    unit_price = round(
        random.uniform(5, 1500), 2
    )

    total = round(quantity * unit_price, 2)

    records.append({
        "purchase_id": f"PO-{i:05d}",
        "date": fake.date_between(
            start_date="-1y",
            end_date="today"
        ).isoformat(),
        "supplier": random.choice(suppliers),
        "item": random.choice(items),
        "quantity": quantity,
        "unit_price": unit_price,
        "total": total
    })

# Create DataFrame
df = pd.DataFrame(records)

# Save clean dataset
output_path = DATA_DIR / "clean_purchases.csv"

df.to_csv(output_path, index=False)

# Display results
print("Clean dataset generated successfully!")
print(f"Total records: {len(df)}")
print(f"Total columns: {len(df.columns)}")
print(f"Missing values: {df.isna().sum().sum()}")
print(f"Duplicate rows: {df.duplicated().sum()}")
print(f"File saved at: {output_path}")

print("\nFirst 5 records:")
print(df.head())
