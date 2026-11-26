
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]

TEST_DIR = BASE_DIR / "tests"
REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

ANSWER_KEY = TEST_DIR / "answer_key.csv"

TARGET_ACCURACY = 90.0

KEY_COLUMNS = ["file_name", "original_header"]


def evaluate_mapper(method_name, result_file):

    answer_key = pd.read_csv(ANSWER_KEY)
    predictions = pd.read_csv(result_file)

    # Compare predictions against correct answers
    merged = answer_key.merge(
        predictions,
        on=KEY_COLUMNS,
        how="outer",
        validate="one_to_one",
        indicator=True
    )

    # Validate that all expected headers are present
    if not merged["_merge"].eq("both").all():
        raise ValueError(
            f"{method_name}: Missing or unexpected headers."
        )

    merged["is_correct"] = (
        merged["standard_field"]
        == merged["mapped_field"]
    )

    merged["is_unmapped"] = (
        merged["mapped_field"] == "UNMAPPED"
    )

    merged["is_incorrect"] = (
        ~merged["is_correct"]
        & ~merged["is_unmapped"]
    )

    total = len(merged)

    correct = int(merged["is_correct"].sum())

    incorrect = int(merged["is_incorrect"].sum())

    unmapped = int(merged["is_unmapped"].sum())

    auto_mapped = total - unmapped

    accuracy = (correct / total) * 100

    precision = (
        (correct / auto_mapped) * 100
        if auto_mapped > 0 else 0
    )

    coverage = (auto_mapped / total) * 100

    average_confidence = merged["confidence"].mean()

    high_confidence_errors = int(
        (
            merged["is_incorrect"]
            & (merged["confidence"] >= 80)
        ).sum()
    )

    merged["method"] = method_name

    merged = merged.drop(columns=["_merge"])

    file_prefix = (
        method_name.lower().replace(" ", "_")
    )

    # Save detailed evaluation
    merged.to_csv(
        REPORT_DIR / f"{file_prefix}_evaluation.csv",
        index=False
    )

    # Save incorrect and unmapped examples
    errors = merged[
        ~merged["is_correct"]
    ].copy()

    errors.to_csv(
        REPORT_DIR / f"{file_prefix}_errors.csv",
        index=False
    )

    summary = {
        "method": method_name,
        "total_headers": total,
        "correct_mappings": correct,
        "incorrect_mappings": incorrect,
        "unmapped_headers": unmapped,
        "accuracy_percent": round(accuracy, 2),
        "precision_percent": round(precision, 2),
        "coverage_percent": round(coverage, 2),
        "average_confidence": round(
            average_confidence, 2
        ),
        "high_confidence_errors": high_confidence_errors,
        "target_status": (
            "PASS"
            if accuracy >= TARGET_ACCURACY
            else "FAIL"
        )
    }

    return summary, merged, errors


def main():

    methods = {
        "Rule Based":
            REPORT_DIR / "rule_based_results.csv",

        "RapidFuzz":
            REPORT_DIR / "fuzzy_mapping_results.csv"
    }

    summaries = []
    detailed_results = []
    all_errors = []

    for method_name, result_file in methods.items():

        summary, details, errors = evaluate_mapper(
            method_name,
            result_file
        )

        summaries.append(summary)
        detailed_results.append(details)
        all_errors.append(errors)

    comparison = pd.DataFrame(summaries)

    details_df = pd.concat(
        detailed_results,
        ignore_index=True
    )

    errors_df = pd.concat(
        all_errors,
        ignore_index=True
    )

    comparison.to_csv(
        REPORT_DIR / "algorithm_comparison.csv",
        index=False
    )

    # Create final Excel evaluation report
    excel_file = (
        REPORT_DIR / "mapper_evaluation_report.xlsx"
    )

    with pd.ExcelWriter(
        excel_file,
        engine="openpyxl"
    ) as writer:

        comparison.to_excel(
            writer,
            sheet_name="Algorithm Comparison",
            index=False
        )

        details_df.to_excel(
            writer,
            sheet_name="Detailed Results",
            index=False
        )

        errors_df.to_excel(
            writer,
            sheet_name="Mapping Errors",
            index=False
        )

    print("=" * 60)
    print("COLUMN MAPPING ACCURACY EVALUATION")
    print("=" * 60)

    for summary in summaries:

        print(f"\nMethod: {summary['method']}")

        print(
            f"Total headers: "
            f"{summary['total_headers']}"
        )

        print(
            f"Correct mappings: "
            f"{summary['correct_mappings']}"
        )

        print(
            f"Incorrect mappings: "
            f"{summary['incorrect_mappings']}"
        )

        print(
            f"Unmapped headers: "
            f"{summary['unmapped_headers']}"
        )

        print(
            f"Accuracy: "
            f"{summary['accuracy_percent']}%"
        )

        print(
            f"Precision: "
            f"{summary['precision_percent']}%"
        )

        print(
            f"Coverage: "
            f"{summary['coverage_percent']}%"
        )

        print(
            f"Average confidence: "
            f"{summary['average_confidence']}"
        )

        print(
            f"High confidence errors: "
            f"{summary['high_confidence_errors']}"
        )

        print(
            f"Target status: "
            f"{summary['target_status']}"
        )

    ranked = comparison.sort_values(
        ["accuracy_percent", "precision_percent"],
        ascending=False
    )

    best_method = ranked.iloc[0]

    print("\n" + "=" * 60)
    print("ALGORITHM COMPARISON")
    print("=" * 60)

    print(comparison.to_string(index=False))

    print(
        f"\nTop ranked method: "
        f"{best_method['method']}"
    )

    print(
        f"Best accuracy: "
        f"{best_method['accuracy_percent']}%"
    )

    print(f"\nExcel report saved to: {excel_file}")


if __name__ == "__main__":
    main()
