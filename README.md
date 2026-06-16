# SDET Take-Home Screening Exercise

**Candidate:** Anandababu M  
**Role:** Automation Engineer / SDET  
**Language:** Python 3.10+  
**Testing Framework:** Pytest

**Repository Structure**
sdet-take-home/
├── README.md
├── AI_TRANSCRIPT.md
├── answers.sql
├── expected_orders.csv
├── actual_orders.csv
├── compare_headers.py
└── test_compare_headers.py

---
## Prerequisites

- Python 3.10 or above
- Git
  
## Setup — Virtual Environment (Recommended)

### Step 1 — Create virtual environment

```bash
# Windows
python -m venv venv

# Mac / Linux
python3 -m venv venv
```

### Step 2 — Activate virtual environment

```bash
# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

You should see `(venv)` appear at the start of your terminal prompt.

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Run the CSV comparison tool


```bash
python compare_headers.py expected_orders.csv actual_orders.csv
```

**Example output:**

```
--------------------------------------------------
CSV Header Comparison
  Expected : expected_orders.csv
  Actual   : actual_orders.csv
--------------------------------------------------

Only in expected_orders.csv:
  amount
  created_at
  country

Only in actual_orders.csv:
  total_amount
  processed_at
  country_code

Common headers:
  order_id
  customer_id
  currency
  status

Common headers in same relative order: true
--------------------------------------------------
```

---

## How to Run the Tests

Run all tests:

```bash
pytest test_compare_headers.py -v
```

Expected result: **12 tests pass**.

---
# Generate HTML test report (impressive for TCS reviewer)
pytest test_compare_headers.py -v --html=report.html --self-contained-html

## SQL Answers

Full SQL is in `answers.sql`. Below is a summary of each query and the approach chosen.

### Task 1 — Price Changes

```sql
SELECT t.product_id, t.product_name, y.price AS old_price, t.price AS new_price
FROM products_yesterday y
INNER JOIN products_today t ON y.product_id = t.product_id
WHERE y.price <> t.price;
```

**Why INNER JOIN:** We only care about products that exist in *both* tables. If a product was removed or added, a price comparison is not meaningful. INNER JOIN naturally filters those rows out.

### Task 2 — New Products

```sql
SELECT t.product_id, t.product_name, t.price, t.status
FROM products_today t
LEFT JOIN products_yesterday y ON t.product_id = y.product_id
WHERE y.product_id IS NULL;
```

**Why LEFT JOIN + IS NULL:** This is a standard "anti-join" pattern. It is widely supported and readable. `NOT EXISTS` is an equally valid alternative that can perform better on large datasets.

### Task 3 — Missing Products

Same anti-join pattern, reversed direction:

```sql
SELECT y.product_id, y.product_name, y.price, y.status
FROM products_yesterday y
LEFT JOIN products_today t ON y.product_id = t.product_id
WHERE t.product_id IS NULL;
```

### Task 4 — Status Changes

```sql
SELECT t.product_id, t.product_name, y.status AS old_status, t.status AS new_status
FROM products_yesterday y
INNER JOIN products_today t ON y.product_id = t.product_id
WHERE y.status <> t.status;
```

### Task 5 — Short Explanations

**1. Why INNER JOIN or LEFT JOIN?**

- INNER JOIN is used when we only want rows that exist in *both* tables (price/status changes).
- LEFT JOIN + IS NULL is used for set-difference queries (new or missing products).
- NOT EXISTS is a semantically equivalent alternative to LEFT JOIN + IS NULL. On large datasets, the query planner may choose different execution plans; in practice either is fine.

**2. What would change if product_id was not unique?**

If `product_id` is not unique, joins would produce a Cartesian product between all matching rows. For example, if product 1002 appears twice in yesterday and twice in today, the INNER JOIN produces 4 rows. This can lead to duplicate or inflated results. To handle non-unique keys, you would need to either:
- Deduplicate first using a CTE with `ROW_NUMBER()`, or
- Use `GROUP BY` and aggregate (e.g., `MAX(price)`) before joining.

**3. NULL values in price or status?**

The comparison `y.price <> t.price` returns NULL (not TRUE) when either side is NULL, so rows with NULL prices are silently excluded. To handle this correctly:

```sql
WHERE y.price IS DISTINCT FROM t.price   -- PostgreSQL
-- or
WHERE (y.price <> t.price OR y.price IS NULL OR t.price IS NULL)  -- standard SQL
```

The same applies to the status column.

---

## API Test Cases (Part C)

**Endpoint:** `GET /api/orders/{order_id}`

| # | Test Name | Input | Expected Result | Why Useful |
|---|-----------|-------|-----------------|------------|
| 1 | Valid order returns 200 with correct fields | `GET /api/orders/ORD-1001` | HTTP 200, `order_id="ORD-1001"`, `status="PAID"` | Validates the happy path and that all response fields are present |
| 2 | Non-existent order returns 404 | `GET /api/orders/ORD-9999` | HTTP 404, meaningful error message | Confirms the API does not return 200 for unknown resources |
| 3 | Malformed order ID returns 400 | `GET /api/orders/INVALID` | HTTP 400 or 404, no 500 | Validates input boundary — IDs that break the ID format |
| 4 | Amount field is a number, not a string | `GET /api/orders/ORD-1001` | `amount` is a JSON number (100.50), not `"100.50"` | Type correctness matters — callers doing arithmetic will break on a string |
| 5 | Timestamp field is ISO 8601 format | `GET /api/orders/ORD-1001` | `created_at` matches `YYYY-MM-DDTHH:MM:SSZ` | Date parsing breaks silently if format changes unexpectedly |

**Automated test (Python requests):**

```python
import requests

def test_get_order_paid():
    base_url = "https://api.example.com"
    response = requests.get(f"{base_url}/api/orders/ORD-1001")

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    body = response.json()
    assert body["order_id"] == "ORD-1001"
    assert body["status"] == "PAID"
    assert isinstance(body["amount"], float), "amount should be a float"
```

---

## Assumptions

1. The CSV files use a single comma as the delimiter. No quoted commas or embedded commas in field values.
2. SQL queries assume a standard relational database. `IS DISTINCT FROM` syntax in the NULL discussion is PostgreSQL-specific; the standard SQL alternative is noted.
3. The API base URL in the automated test is a placeholder.
4. The `read_headers` function reads only the first line; it does not validate data rows.

---

## AI Usage Statement

I used Claude (claude.ai) as an AI assistant for this exercise. The full conversation transcript is included in `AI_TRANSCRIPT.md`.

**What I used AI for:**

- Generating the initial structure of `compare_headers.py`
- Generating the pytest test file structure
- Generating the SQL query templates

**What I reviewed and verified:**

- All SQL queries were checked manually against the provided data tables to confirm expected output rows
- The Python comparison logic (`compare_headers` function) was reviewed and the relative order check logic was verified by me
- All 12 pytest tests were run locally and pass

**What I changed:**

- Adjusted the `same_relative_order` logic to correctly handle the case where there are no common headers (vacuously true rather than raising an error)
- Added the `test_no_common_headers` test case myself after reviewing edge cases
- Expanded the SQL Task 5 NULL explanation to cover `IS DISTINCT FROM`

---

## Candidate Acknowledgement

By submitting this exercise, I confirm that:

1. I have followed the AI usage rules.
2. I have included the full relevant AI transcript in `AI_TRANSCRIPT.md`.
3. I understand the submitted solution.
4. I am able to explain, modify, and debug the solution during the interview.
5. I understand that failure to disclose AI use, or inability to explain the submitted work, may result in rejection.
