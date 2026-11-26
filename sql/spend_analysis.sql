
-- Load cleaned dataset
CREATE OR REPLACE TABLE spend AS
SELECT *
FROM read_csv_auto('data/cleaned/cleaned_spend.csv');

-- 1. Total spending
SELECT ROUND(SUM(federal_action_obligation), 2)
AS total_spend
FROM spend;

-- 2. Supplier count
SELECT COUNT(DISTINCT recipient_name)
AS supplier_count
FROM spend
WHERE recipient_name != 'Unknown';

-- 3. Transaction count
SELECT COUNT(*) AS transaction_count
FROM spend;

-- 4. Monthly spending
SELECT month,
SUM(federal_action_obligation) AS total_spend
FROM spend
GROUP BY month
ORDER BY month;

-- 5. Top 10 suppliers
SELECT recipient_name,
SUM(federal_action_obligation) AS total_spend
FROM spend
WHERE recipient_name != 'Unknown'
GROUP BY recipient_name
ORDER BY total_spend DESC
LIMIT 10;

-- 6. Category spending
SELECT COALESCE(product_or_service_code, 'Unknown')
AS category,
SUM(federal_action_obligation) AS total_spend
FROM spend
GROUP BY category
ORDER BY total_spend DESC;

-- 7. Supplier concentration
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
FROM top_suppliers;
