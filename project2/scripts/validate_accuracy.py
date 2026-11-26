
import pandas as pd
from pathlib import Path

# Project directories
BASE_DIR = Path(__file__).resolve().parents[1]
TEST_DIR = BASE_DIR / "tests"
REPORT_DIR = BASE_DIR / "reports"

# Load expected and detected errors
expected = pd.read_csv(
    TEST_DIR / "answer_key.csv"
)

detected = pd.read_csv(
    REPORT_DIR / "detected_errors.csv"
)

# Columns used for exact comparison
columns = [
    "file",
    "row_number",
    "column",
    "error_type"
]

# Convert records into sets
expected_set = set(
    expected[columns].itertuples(
        index=False, name=None
    )
)

detected_set = set(
    detected[columns].itertuples(
        index=False, name=None
    )
)

# Compare results
true_positives = expected_set & detected_set

false_positives = detected_set - expected_set

false_negatives = expected_set - detected_set

TP = len(true_positives)
FP = len(false_positives)
FN = len(false_negatives)

# Calculate evaluation metrics
precision = (
    TP / (TP + FP)
    if TP + FP > 0 else 0
)

recall = (
    TP / (TP + FN)
    if TP + FN > 0 else 0
)

f1_score = (
    2 * precision * recall / (precision + recall)
    if precision + recall > 0 else 0
)

# Check clean dataset
clean_errors = len(
    detected[
        detected["file"] == "clean_purchases.csv"
    ]
)

# Final test status
passed = (
    len(expected_set) > 0
    and FP == 0
    and FN == 0
    and clean_errors == 0
)

status = "PASS" if passed else "FAIL"

# Display results
print("=" * 60)
print("DATA QUALITY CHECKER - ACCURACY TEST")
print("=" * 60)

print("Expected errors:", len(expected_set))
print("Detected errors:", len(detected_set))

print("\nTrue positives:", TP)
print("False positives:", FP)
print("False negatives:", FN)

print(f"\nPrecision: {precision:.2%}")
print(f"Recall: {recall:.2%}")
print(f"F1 Score: {f1_score:.2%}")

print("\nClean dataset errors:", clean_errors)

print("\nFINAL TEST RESULT:", status)

# Save evaluation report
metrics = pd.DataFrame({
    "Metric": [
        "Expected Errors",
        "Detected Errors",
        "True Positives",
        "False Positives",
        "False Negatives",
        "Precision (%)",
        "Recall (%)",
        "F1 Score (%)",
        "Clean Dataset Errors",
        "Final Test Result"
    ],
    "Value": [
        len(expected_set),
        len(detected_set),
        TP,
        FP,
        FN,
        round(precision * 100, 2),
        round(recall * 100, 2),
        round(f1_score * 100, 2),
        clean_errors,
        status
    ]
})

metrics.to_csv(
    REPORT_DIR / "accuracy_report.csv",
    index=False
)

# Save unexpected errors
pd.DataFrame(
    sorted(false_positives),
    columns=columns
).to_csv(
    REPORT_DIR / "false_positives.csv",
    index=False
)

# Save missed errors
pd.DataFrame(
    sorted(false_negatives),
    columns=columns
).to_csv(
    REPORT_DIR / "false_negatives.csv",
    index=False
)

print("\nAccuracy reports saved successfully.")
print("=" * 60)
