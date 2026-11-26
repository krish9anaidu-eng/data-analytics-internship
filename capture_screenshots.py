
from playwright.sync_api import sync_playwright
from pathlib import Path

REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)

URL = "http://localhost:8505/"

screenshots = [
    (
        "monthly_spending.png",
        "Scroll to the Monthly Spending chart"
    ),
    (
        "supplier_category_analysis.png",
        "Scroll to the Supplier and Category charts"
    ),
    (
        "filtered_dashboard.png",
        "Apply a supplier or category filter"
    )
]

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page(
        viewport={"width": 1920, "height": 1080},
        device_scale_factor=1
    )

    page.goto(URL)
    page.wait_for_timeout(10000)

    for filename, instruction in screenshots:

        print("\n" + "=" * 50)
        print(instruction)

        input("Press ENTER when the dashboard is ready: ")

        page.wait_for_timeout(3000)

        page.screenshot(
            path=str(REPORT_DIR / filename)
        )

        print(f"Screenshot saved: {filename}")

    browser.close()

print("\nALL SCREENSHOTS COMPLETED")

