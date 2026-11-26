
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
REPORT_DIR = BASE_DIR / "reports"
DATA_DIR = BASE_DIR / "data"
TEST_DIR = BASE_DIR / "tests"

TARGET_ACCURACY = 90

comparison = pd.read_csv(
    REPORT_DIR / "algorithm_comparison.csv"
)

answer_key = pd.read_csv(
    TEST_DIR / "answer_key.csv"
)

csv_files = list(
    DATA_DIR.glob("procurement_*.csv")
)

best = comparison.sort_values(
    ["accuracy_percent", "high_confidence_errors"],
    ascending=[False, True]
).iloc[0]

checks = {
    "20 synthetic datasets": len(csv_files) == 20,

    "160 expected mappings": len(answer_key) == 160,

    "Both algorithms evaluated": (
        set(comparison["method"])
        == {"Rule Based", "RapidFuzz"}
    ),

    "All headers evaluated": (
        comparison["total_headers"].eq(160).all()
    ),

    "Minimum 90% accuracy": (
        best["accuracy_percent"] >= TARGET_ACCURACY
    ),

    "No high-confidence incorrect mappings": (
        best["high_confidence_errors"] == 0
    ),

    "Excel evaluation report exists": (
        REPORT_DIR / "mapper_evaluation_report.xlsx"
    ).exists()
}

print("=" * 60)
print("PROJECT 3 - FINAL VALIDATION")
print("=" * 60)

for check, passed in checks.items():

    status = "PASS" if passed else "FAIL"

    print(f"{status}: {check}")

print("\nBEST PERFORMING ALGORITHM")
print("-" * 60)

print(f"Method: {best['method']}")
print(f"Accuracy: {best['accuracy_percent']}%")
print(f"Precision: {best['precision_percent']}%")
print(f"Coverage: {best['coverage_percent']}%")
print(f"Correct mappings: {best['correct_mappings']}")
print(f"Incorrect mappings: {best['incorrect_mappings']}")
print(f"Unmapped headers: {best['unmapped_headers']}")
print(f"High confidence errors: {best['high_confidence_errors']}")

validation = pd.DataFrame([
    {
        "validation_check": check,
        "status": "PASS" if passed else "FAIL"
    }
    for check, passed in checks.items()
])

validation.to_csv(
    REPORT_DIR / "final_validation.csv",
    index=False
)

print("\n" + "=" * 60)

if all(checks.values()):
    print("PROJECT 3 VALIDATION PASSED")
else:
    print("PROJECT 3 REQUIRES FURTHER REVIEW")

print("=" * 60)

