
import pandas as pd
from pathlib import Path

from openpyxl.styles import (
    Font,
    PatternFill,
    Alignment
)

from openpyxl.chart import BarChart, Reference
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.utils import get_column_letter

# Project directories
BASE_DIR = Path(__file__).resolve().parents[1]
REPORT_DIR = BASE_DIR / "reports"

# Load existing reports
summary = pd.read_csv(
    REPORT_DIR / "quality_summary.csv"
)

errors = pd.read_csv(
    REPORT_DIR / "detected_errors.csv"
)

# Create error breakdown
breakdown = (
    errors["error_type"]
    .value_counts()
    .rename_axis("Error Type")
    .reset_index(name="Error Count")
)

# Methodology documentation
methodology = pd.DataFrame({
    "Topic": [
        "Project",
        "Objective",
        "Data Source",
        "Quality Score Formula",
        "Missing Values",
        "Negative Prices",
        "Zero Prices",
        "Incorrect Totals",
        "Duplicate Records",
        "Invalid Dates",
        "Future Dates",
        "Invalid Numbers",
        "Excellent",
        "Good",
        "Needs Improvement",
        "Poor",
        "Row Number Convention"
    ],

    "Description": [
        "Project 2 - Automated Data Quality Checker",
        "Automatically detect purchase data errors",
        "Synthetic purchase records generated using Faker",
        "(Clean rows / Total rows) x 100",
        "Identify blank or missing required fields",
        "Identify unit prices below zero",
        "Identify unit prices equal to zero",
        "Flag calculation differences above $0.01",
        "Identify repeated rows after the first occurrence",
        "Identify invalid dates or incorrect date formats",
        "Identify dates later than today",
        "Identify non-numeric values in numeric columns",
        "Score equals 100",
        "Score from 95 to below 100",
        "Score from 80 to below 95",
        "Score below 80",
        "CSV row numbers include the header as row 1"
    ]
})

# Output Excel file
output_path = (
    REPORT_DIR / "data_quality_report.xlsx"
)

with pd.ExcelWriter(
    output_path,
    engine="openpyxl"
) as writer:

    summary.to_excel(
        writer,
        sheet_name="Quality Summary",
        index=False
    )

    errors.to_excel(
        writer,
        sheet_name="Detected Errors",
        index=False
    )

    breakdown.to_excel(
        writer,
        sheet_name="Error Breakdown",
        index=False
    )

    methodology.to_excel(
        writer,
        sheet_name="Methodology",
        index=False
    )

    workbook = writer.book

    # Format every worksheet
    for sheet in workbook.worksheets:

        sheet.freeze_panes = "A2"

        sheet.auto_filter.ref = sheet.dimensions

        # Header formatting
        for cell in sheet[1]:

            cell.fill = PatternFill(
                fill_type="solid",
                fgColor="17365D"
            )

            cell.font = Font(
                color="FFFFFF",
                bold=True
            )

            cell.alignment = Alignment(
                horizontal="center",
                vertical="center"
            )

        sheet.row_dimensions[1].height = 28

        # Automatically adjust column widths
        for column in sheet.columns:

            max_length = max(
                len(str(cell.value))
                if cell.value is not None else 0
                for cell in column
            )

            column_letter = get_column_letter(
                column[0].column
            )

            sheet.column_dimensions[
                column_letter
            ].width = min(max_length + 4, 85)

        # Alternating row colors
        for row in sheet.iter_rows(min_row=2):

            for cell in row:

                if cell.row % 2 == 0:

                    cell.fill = PatternFill(
                        fill_type="solid",
                        fgColor="EAF1F8"
                    )

    # Quality Summary formatting
    summary_sheet = workbook["Quality Summary"]

    for row in range(
        2, summary_sheet.max_row + 1
    ):

        summary_sheet[f"F{row}"].number_format = "0.00"

    # Conditional formatting for quality scores
    summary_sheet.conditional_formatting.add(
        f"F2:F{summary_sheet.max_row}",

        ColorScaleRule(
            start_type="num",
            start_value=0,
            start_color="F8696B",

            mid_type="num",
            mid_value=80,
            mid_color="FFEB84",

            end_type="num",
            end_value=100,
            end_color="63BE7B"
        )
    )

    # Quality score chart
    score_chart = BarChart()

    score_chart.title = "Dataset Quality Scores"
    score_chart.y_axis.title = "Quality Score"
    score_chart.x_axis.title = "Dataset"

    score_chart.y_axis.scaling.min = 0
    score_chart.y_axis.scaling.max = 100

    score_chart.width = 24
    score_chart.height = 12

    score_chart.add_data(
        Reference(
            summary_sheet,
            min_col=6,
            min_row=1,
            max_row=summary_sheet.max_row
        ),
        titles_from_data=True
    )

    score_chart.set_categories(
        Reference(
            summary_sheet,
            min_col=1,
            min_row=2,
            max_row=summary_sheet.max_row
        )
    )

    score_chart.legend = None

    summary_sheet.add_chart(
        score_chart, "A11"
    )

    # Error breakdown chart
    error_sheet = workbook["Error Breakdown"]

    error_chart = BarChart()

    error_chart.title = "Detected Errors by Type"
    error_chart.type = "bar"

    error_chart.x_axis.title = "Number of Errors"
    error_chart.y_axis.title = "Error Type"

    error_chart.width = 22
    error_chart.height = 12

    error_chart.add_data(
        Reference(
            error_sheet,
            min_col=2,
            min_row=1,
            max_row=error_sheet.max_row
        ),
        titles_from_data=True
    )

    error_chart.set_categories(
        Reference(
            error_sheet,
            min_col=1,
            min_row=2,
            max_row=error_sheet.max_row
        )
    )

    error_chart.legend = None

    error_sheet.add_chart(
        error_chart, "D2"
    )

# Completion message
print("=" * 60)
print("EXCEL DATA QUALITY REPORT GENERATED")
print("=" * 60)

print("Worksheets created: 4")
print("Datasets analyzed:", len(summary))
print("Total records:", summary["total_rows"].sum())
print("Total errors:", len(errors))

print("\nReport saved at:")
print(output_path)

print("=" * 60)

