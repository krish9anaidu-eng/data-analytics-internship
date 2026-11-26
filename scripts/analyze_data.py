
import duckdb

# Create database connection
con = duckdb.connect()

# Load cleaned dataset
con.execute("""
CREATE TABLE spend AS
SELECT * FROM read_csv_auto(
    'data/cleaned/cleaned_spend.csv'
)
""")

# 1. Total spend
print("\nTOTAL SPEND")

print(con.execute("""
SELECT ROUND(SUM(federal_action_obligation), 2)
AS total_spend
FROM spend
""").df())

# 2. Total suppliers
print("\nTOTAL SUPPLIERS")

print(con.execute("""
SELECT COUNT(DISTINCT recipient_name)
AS total_suppliers
FROM spend
WHERE recipient_name != 'Unknown'
""").df())

# 3. Total transactions
print("\nTOTAL TRANSACTIONS")

print(con.execute("""
SELECT COUNT(*) AS total_transactions
FROM spend
""").df())

# 4. Monthly spending
print("\nMONTHLY SPENDING")

print(con.execute("""
SELECT month,
ROUND(SUM(federal_action_obligation), 2)
AS total_spend
FROM spend
GROUP BY month
ORDER BY month
""").df())

# 5. Top 10 suppliers
print("\nTOP 10 SUPPLIERS")

print(con.execute("""
SELECT recipient_name,
ROUND(SUM(federal_action_obligation), 2)
AS total_spend
FROM spend
WHERE recipient_name != 'Unknown'
GROUP BY recipient_name
ORDER BY total_spend DESC
LIMIT 10
""").df())

# 6. Spending by category
print("\nSPENDING BY CATEGORY")

print(con.execute("""
SELECT product_or_service_code,
ROUND(SUM(federal_action_obligation), 2)
AS total_spend
FROM spend
GROUP BY product_or_service_code
ORDER BY total_spend DESC
LIMIT 10
""").df())

# 7. Pareto analysis
print("\nTOP 10 SUPPLIER SPEND PERCENTAGE")

print(con.execute("""
WITH top_suppliers AS (
    SELECT recipient_name,
    SUM(federal_action_obligation) AS amount
    FROM spend
    WHERE recipient_name != 'Unknown'
    GROUP BY recipient_name
    ORDER BY amount DESC
    LIMIT 10
)
SELECT ROUND(
    100.0 * SUM(amount) /
    NULLIF((SELECT SUM(federal_action_obligation)
    FROM spend), 0), 2
) AS top_10_percentage
FROM top_suppliers
""").df())

con.close()
