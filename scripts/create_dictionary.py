
import pandas as pd
from pathlib import Path

df = pd.read_csv(
    "data/cleaned/cleaned_spend.csv",
    low_memory=False
)

descriptions = {
    "action_date": "Date of the contract transaction",
    "federal_action_obligation": "Change in federal obligated amount",
    "recipient_name": "Name of the supplier or recipient",
    "product_or_service_code": "Product or service classification code",
    "product_or_service_code_description": "Description of product or service",
    "awarding_agency_name": "Government agency awarding the contract",
    "month": "Transaction month in YYYY-MM format",
    "year": "Transaction year",
    "award_id_piid": "Procurement instrument identifier"
}

dictionary = []

for column in df.columns:

    examples = df[column].dropna()

    dictionary.append({
        "Column Name": column,
        "Data Type": str(df[column].dtype),
        "Description": descriptions.get(
            column, "Needs documentation"
        ),
        "Example Value": (
            str(examples.iloc[0])
            if not examples.empty else ""
        ),
        "Missing Values": df[column].isna().sum(),
        "Unique Values": df[column].nunique()
    })

result = pd.DataFrame(dictionary)

Path("reports").mkdir(exist_ok=True)

result.to_excel(
    "reports/data_dictionary.xlsx",
    index=False
)

print("Data dictionary created successfully!")
