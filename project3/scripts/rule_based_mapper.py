
import pandas as pd
from pathlib import Path
from header_cleaner import clean_header
from standard_fields import STANDARD_FIELDS


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

CONFIDENCE_THRESHOLD = 80


# Procurement terminology and common abbreviations
ALIASES = {
    "description": [
        "item desc",
        "product name",
        "item description",
        "material description",
        "product details"
    ],
    "quantity": [
        "qty",
        "units",
        "qty ordered",
        "order quantity",
        "unit count"
    ],
    "unit_price": [
        "unit cost",
        "price each",
        "cost per unit",
        "price unit",
        "rate"
    ],
    "total_spend": [
        "ext amt",
        "total amount",
        "total cost",
        "extended price",
        "line total"
    ],
    "supplier": [
        "vendor",
        "supplier name",
        "seller",
        "vendor name"
    ],
    "manufacturer": [
        "mfr",
        "maker",
        "mfg name",
        "manufacturer name",
        "producer"
    ],
    "part_number": [
        "part no",
        "sku",
        "part num",
        "product code",
        "item code"
    ],
    "date": [
        "purchase date",
        "order date",
        "transaction date",
        "invoice date",
        "po date"
    ]
}


def calculate_score(header, standard_field):

    header = clean_header(header)
    standard = clean_header(standard_field)

    if not header:
        return 0

    # Rule 1: Exact standard field match
    if header == standard:
        return 100

    aliases = [
        clean_header(alias)
        for alias in ALIASES.get(standard_field, [])
    ]

    # Rule 2: Known synonym match
    if header in aliases:
        return 95

    candidates = [standard] + aliases

    header_words = set(header.split())

    best_score = 0

    for candidate in candidates:

        candidate_words = set(candidate.split())

        # Rule 3: Complete keyword match
        if candidate_words.issubset(header_words):
            best_score = max(best_score, 85)

        # Rule 4: Partial keyword match
        elif header_words.intersection(candidate_words):
            best_score = max(best_score, 65)

    return best_score


def map_headers(headers):

    candidates = []

    # Score every possible header-field combination
    for header in headers:

        for field in STANDARD_FIELDS:

            score = calculate_score(header, field)

            candidates.append(
                (header, field, score)
            )

    # Highest confidence matches first
    candidates.sort(
        key=lambda item: item[2],
        reverse=True
    )

    used_headers = set()
    used_fields = set()
    results = []

    # Enforce one-to-one mapping
    for header, field, score in candidates:

        if score < CONFIDENCE_THRESHOLD:
            continue

        if header in used_headers:
            continue

        if field in used_fields:
            continue

        results.append({
            "original_header": header,
            "cleaned_header": clean_header(header),
            "mapped_field": field,
            "confidence": score,
            "status": "Auto Mapped"
        })

        used_headers.add(header)
        used_fields.add(field)

    # Flag unmatched headers for human review
    for header in headers:

        if header not in used_headers:

            best_field = max(
                STANDARD_FIELDS,
                key=lambda field: calculate_score(
                    header, field
                )
            )

            best_score = calculate_score(
                header, best_field
            )

            results.append({
                "original_header": header,
                "cleaned_header": clean_header(header),
                "mapped_field": "UNMAPPED",
                "confidence": best_score,
                "status": "Needs Human Review"
            })

    return results


def process_all_files():

    all_results = []

    csv_files = sorted(
        DATA_DIR.glob("procurement_*.csv")
    )

    for file in csv_files:

        df = pd.read_csv(file, nrows=0)

        mappings = map_headers(
            list(df.columns)
        )

        for mapping in mappings:

            mapping["file_name"] = file.name
            all_results.append(mapping)

        print(f"Processed: {file.name}")

    result_df = pd.DataFrame(all_results)

    result_df = result_df[
        [
            "file_name",
            "original_header",
            "cleaned_header",
            "mapped_field",
            "confidence",
            "status"
        ]
    ]

    output_file = REPORT_DIR / "rule_based_results.csv"

    result_df.to_csv(output_file, index=False)

    auto_mapped = (
        result_df["status"] == "Auto Mapped"
    ).sum()

    human_review = (
        result_df["status"] == "Needs Human Review"
    ).sum()

    print("\n" + "=" * 50)
    print("RULE-BASED MAPPING COMPLETED")
    print("=" * 50)

    print(f"Files processed: {len(csv_files)}")
    print(f"Total headers: {len(result_df)}")
    print(f"Automatically mapped: {auto_mapped}")
    print(f"Needs human review: {human_review}")
    print(f"Confidence threshold: {CONFIDENCE_THRESHOLD}")

    print("\nSample mappings:")
    print(result_df.head(15).to_string(index=False))

    print(f"\nReport saved to: {output_file}")


if __name__ == "__main__":

    process_all_files()

