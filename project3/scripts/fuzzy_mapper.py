
import pandas as pd
from pathlib import Path
from rapidfuzz import fuzz

from header_cleaner import clean_header
from standard_fields import STANDARD_FIELDS
from rule_based_mapper import ALIASES


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

CONFIDENCE_THRESHOLD = 80


def calculate_fuzzy_score(header, standard_field):

    cleaned_header = clean_header(header)

    if not cleaned_header:
        return 0.0

    candidates = [standard_field]

    candidates.extend(
        ALIASES.get(standard_field, [])
    )

    scores = []

    for candidate in candidates:

        cleaned_candidate = clean_header(candidate)

        score = fuzz.WRatio(
            cleaned_header,
            cleaned_candidate
        )

        scores.append(score)

    return round(max(scores), 2)


def map_headers(headers):

    candidates = []

    for header in headers:

        for field in STANDARD_FIELDS:

            score = calculate_fuzzy_score(
                header,
                field
            )

            candidates.append(
                (header, field, score)
            )

    # Sort by highest confidence
    candidates.sort(
        key=lambda item: item[2],
        reverse=True
    )

    used_headers = set()
    used_fields = set()

    results = []

    # One-to-one column mapping
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

    # Flag unmatched headers
    for header in headers:

        if header not in used_headers:

            best_field = max(
                STANDARD_FIELDS,
                key=lambda field: calculate_fuzzy_score(
                    header,
                    field
                )
            )

            best_score = calculate_fuzzy_score(
                header,
                best_field
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

    output_file = (
        REPORT_DIR / "fuzzy_mapping_results.csv"
    )

    result_df.to_csv(
        output_file,
        index=False
    )

    auto_mapped = (
        result_df["status"] == "Auto Mapped"
    ).sum()

    human_review = (
        result_df["status"] == "Needs Human Review"
    ).sum()

    average_confidence = (
        result_df["confidence"].mean()
    )

    print("\n" + "=" * 50)
    print("RAPIDFUZZ MAPPING COMPLETED")
    print("=" * 50)

    print(f"Files processed: {len(csv_files)}")
    print(f"Total headers: {len(result_df)}")
    print(f"Automatically mapped: {auto_mapped}")
    print(f"Needs human review: {human_review}")

    print(
        f"Average confidence: "
        f"{average_confidence:.2f}"
    )

    print(
        f"Confidence threshold: "
        f"{CONFIDENCE_THRESHOLD}"
    )

    print("\nSample mappings:")

    print(
        result_df.head(15).to_string(index=False)
    )

    print(f"\nReport saved to: {output_file}")


if __name__ == "__main__":

    process_all_files()
