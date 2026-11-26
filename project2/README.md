
# Project 2 - Automated Data Quality Checker

## Project Overview

An automated Python-based data quality validation
tool designed to identify inconsistencies, missing
values, invalid records, and calculation errors
in procurement datasets.

## Business Objective

Improve procurement data reliability by automating
data validation, reducing manual verification,
and providing actionable data quality reports.

## Technologies Used

- Python
- Pandas
- Faker
- OpenPyXL
- Microsoft Excel
- Git
- Visual Studio Code

## Dataset

- 1,000 synthetic purchase records
- Five intentionally corrupted datasets
- 6,010 total records across all datasets
- 60 intentionally planted errors
- Ground truth answer key for accuracy testing

## Validation Rules

1. Missing required values
2. Negative unit prices
3. Zero unit prices
4. Incorrect purchase totals
5. Duplicate records
6. Invalid date formats
7. Future dates
8. Invalid numeric values

## Quality Score Formula

Quality Score = (Clean Rows / Total Rows) * 100

Rows containing multiple errors are counted
only once when calculating the quality score.

## Quality Score Results

| Dataset | Score |
|---|---:|
| Clean Purchases | 100.00% |
| Missing Values | 99.00% |
| Invalid Prices | 99.00% |
| Incorrect Totals | 99.00% |
| Duplicate Records | 99.01% |
| Mixed Errors | 98.00% |

## Accuracy Testing Results

- Expected Errors: 60
- Correctly Detected Errors: 60
- False Positives: 0
- False Negatives: 0
- Precision: 100%
- Recall: 100%
- F1 Score: 100%
- Clean Dataset Errors: 0
- Final Test Result: PASS

These results apply to the generated synthetic
test datasets.

## Project Structure

project2/
    data/
    scripts/
        generate_data.py
        generate_errors.py
        quality_checker.py
        quality_score.py
        generate_report.py
        validate_accuracy.py
    tests/
    reports/
    README.md

## Execution Instructions

Run the following commands from the repository root:

    pip install pandas faker openpyxl

    python project2/scripts/generate_data.py
    python project2/scripts/generate_errors.py
    python project2/scripts/quality_checker.py
    python project2/scripts/quality_score.py
    python project2/scripts/generate_report.py
    python project2/scripts/validate_accuracy.py

## Deliverables

- Clean procurement dataset
- Five corrupted test datasets
- Ground truth answer key
- Automated data validation engine
- Data quality score report
- Excel data quality report
- Accuracy evaluation report
- False positive and false negative reports

## Business Benefits

- Automated procurement data validation
- Reduced manual data review
- Improved data reliability
- Identification of financial calculation errors
- Standardized quality reporting
- Reproducible validation and testing

## Future Enhancements

- Fuzzy supplier name matching
- Streamlit interactive dashboard
- Database integration
- Automated email notifications
- Configurable validation rules
- Real-time data quality monitoring

## Conclusion

The automated data quality checker successfully
detected all 60 intentionally introduced errors
with zero false positives and zero false negatives
across the synthetic test datasets.
