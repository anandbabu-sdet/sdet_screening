-- ============================================================
-- SDET Screening Exercise — SQL Answers
-- Author: Anandababu M
-- Language: Standard SQL (compatible with PostgreSQL, MySQL, SQLite)
-- ============================================================

-- ---------------------------------------------------------------
-- SQL Task 1 — Products whose PRICE changed from yesterday to today
-- ---------------------------------------------------------------
-- INNER JOIN gives us only products that exist in BOTH tables.
-- We then filter where the price differs.
SELECT
    t.product_id,
    t.product_name,
    y.price AS old_price,
    t.price AS new_price
FROM products_yesterday y
INNER JOIN products_today t
    ON y.product_id = t.product_id
WHERE y.price <> t.price;

-- Expected output:
-- product_id | product_name  | old_price | new_price
-- 1002       | Laptop Stand  | 38.00     | 35.00
-- 1003       | Wireless Mouse| 19.99     | 21.99


-- ---------------------------------------------------------------
-- SQL Task 2 — Products NEW today (exist in today, not in yesterday)
-- ---------------------------------------------------------------
-- LEFT JOIN from today → yesterday, then filter rows where
-- yesterday has no match (NULL on y.product_id).
-- Alternatively NOT EXISTS is semantically cleaner for "does not exist".
SELECT
    t.product_id,
    t.product_name,
    t.price,
    t.status
FROM products_today t
LEFT JOIN products_yesterday y
    ON t.product_id = y.product_id
WHERE y.product_id IS NULL;

-- Alternative using NOT EXISTS (same result, often better optimizer hint):
-- SELECT t.product_id, t.product_name, t.price, t.status
-- FROM products_today t
-- WHERE NOT EXISTS (
--     SELECT 1 FROM products_yesterday y WHERE y.product_id = t.product_id
-- );

-- Expected output:
-- product_id | product_name | price | status
-- 1006       | Webcam       | 59.00 | ACTIVE
-- 1007       | USB Cable    | 7.99  | ACTIVE


-- ---------------------------------------------------------------
-- SQL Task 3 — Products MISSING today (exist in yesterday, not in today)
-- ---------------------------------------------------------------
SELECT
    y.product_id,
    y.product_name,
    y.price,
    y.status
FROM products_yesterday y
LEFT JOIN products_today t
    ON y.product_id = t.product_id
WHERE t.product_id IS NULL;

-- Expected output:
-- product_id | product_name | price | status
-- 1004       | Old Keyboard | 29.99 | DISCONTINUED


-- ---------------------------------------------------------------
-- SQL Task 4 — Products whose STATUS changed
-- ---------------------------------------------------------------
SELECT
    t.product_id,
    t.product_name,
    y.status AS old_status,
    t.status AS new_status
FROM products_yesterday y
INNER JOIN products_today t
    ON y.product_id = t.product_id
WHERE y.status <> t.status;

-- Expected output:
-- product_id | product_name | old_status | new_status
-- 1005       | Notebook     | ACTIVE     | INACTIVE
