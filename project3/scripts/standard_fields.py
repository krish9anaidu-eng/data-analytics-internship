
# Project 3 - Smart Column Mapper
# Define standardized procurement column names

STANDARD_FIELDS = [
    "description",
    "quantity",
    "unit_price",
    "total_spend",
    "supplier",
    "manufacturer",
    "part_number",
    "date"
]


if __name__ == "__main__":
    print("Smart Column Mapper")
    print("-" * 40)

    print("Standard procurement fields:")

    for index, field in enumerate(STANDARD_FIELDS, start=1):
        print(f"{index}. {field}")

    print("-" * 40)
    print(f"Total standard fields: {len(STANDARD_FIELDS)}")
