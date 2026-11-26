
import pandas as pd
import random
from faker import Faker
from pathlib import Path
from standard_fields import STANDARD_FIELDS

fake = Faker()

# Reproducible datasets
Faker.seed(42)
random.seed(42)

# Project directories
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
TEST_DIR = BASE_DIR / "tests"

DATA_DIR.mkdir(parents=True, exist_ok=True)
TEST_DIR.mkdir(parents=True, exist_ok=True)

# Different names for the same standard fields
HEADER_VARIATIONS = {
    "description": [
        "Item Desc.", "Product Name", "Description",
        "Item Description", "Material Desc",
        "Product Details", "ITEM_DESC", "Item Name"
    ],
    "quantity": [
        "Qty", "Units", "Qty Ordered",
        "QUANTITY (EA)", "Order Quantity",
        "QTY_ORDERED", "Unit Count", "Quantity"
    ],
    "unit_price": [
        "Unit Cost", "Price Each", "Unit Price",
        "UNIT_PRICE", "Cost Per Unit",
        "Item Price", "Price/Unit", "Rate"
    ],
    "total_spend": [
        "Ext Amt", "Total Amount", "Total Spend",
        "TOTAL_COST", "Extended Price",
        "Line Total", "Purchase Value", "Total Price"
    ],
    "supplier": [
        "Vendor", "Supplier Name", "Supplier",
        "VENDOR_NAME", "Seller",
        "Vendor Company", "Supplier Details", "Vendor Name"
    ],
    "manufacturer": [
        "Mfr", "Manufacturer Name", "Manufacturer",
        "Maker", "MFG_NAME",
        "Manufacturing Company", "Mfr Name", "Producer"
    ],
    "part_number": [
        "Part No", "SKU", "Part Number",
        "PART_NUM", "Product Code",
        "Item Code", "Material Number", "Part #"
    ],
    "date": [
        "Purchase Date", "Order Date", "Date",
        "PURCHASE_DATE", "Transaction Date",
        "Invoice Date", "PO Date", "Order Dt"
    ]
}

PRODUCTS = [
    "Safety Gloves",
    "Industrial Screws",
    "Laptop",
    "Office Chair",
    "Cleaning Supplies",
    "Steel Pipes",
    "Safety Helmet",
    "Printer Paper",
    "Electrical Cable",
    "Power Drill"
]

answer_key = []

NUM_FILES = 20
ROWS_PER_FILE = 100

for file_number in range(1, NUM_FILES + 1):

    records = []

    for _ in range(ROWS_PER_FILE):

        quantity = random.randint(1, 100)
        unit_price = round(random.uniform(5, 500), 2)

        record = {
            "description": random.choice(PRODUCTS),
            "quantity": quantity,
            "unit_price": unit_price,
            "total_spend": round(quantity * unit_price, 2),
            "supplier": fake.company(),
            "manufacturer": fake.company(),
            "part_number": fake.bothify(
                text="PART-####-??"
            ).upper(),
            "date": fake.date_between(
                start_date="-2y",
                end_date="today"
            ).isoformat()
        }

        records.append(record)

    df = pd.DataFrame(records)

    # Select different headers for each file
    mapping = {
        field: random.choice(HEADER_VARIATIONS[field])
        for field in STANDARD_FIELDS
    }

    filename = f"procurement_{file_number:02d}.csv"

    # Store the correct mappings
    for standard_field, original_header in mapping.items():

        answer_key.append({
            "file_name": filename,
            "original_header": original_header,
            "standard_field": standard_field
        })

    # Rename columns
    df = df.rename(columns=mapping)

    # Shuffle column order to increase difficulty
    columns = list(df.columns)
    random.shuffle(columns)
    df = df[columns]

    # Save CSV file
    df.to_csv(DATA_DIR / filename, index=False)

    print(f"Created: {filename} | Rows: {len(df)}")

# Save answer key
answer_df = pd.DataFrame(answer_key)

answer_df.to_csv(
    TEST_DIR / "answer_key.csv",
    index=False
)

print("\n" + "=" * 45)
print("DATA GENERATION COMPLETED")
print("=" * 45)
print(f"Total CSV files: {NUM_FILES}")
print(f"Rows per file: {ROWS_PER_FILE}")
print(f"Total records: {NUM_FILES * ROWS_PER_FILE}")
print(f"Expected mappings: {len(answer_df)}")
print(f"Answer key: {TEST_DIR / 'answer_key.csv'}")

