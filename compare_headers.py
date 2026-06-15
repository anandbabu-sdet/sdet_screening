"""
compare_headers.py
------------------
CSV Header Comparison Tool

Compares the header row of two CSV files and reports:
  - Headers only in the expected file
  - Headers only in the actual file
  - Headers present in both files
  - Whether common headers appear in the same relative order

Usage:
    python compare_headers.py <expected_csv> <actual_csv>

Example:
    python compare_headers.py expected_orders.csv actual_orders.csv

Author: Anandababu M
"""

import sys
import os


# ──────────────────────────────────────────────
# Core comparison logic (pure functions — easily testable)
# ──────────────────────────────────────────────

def read_headers(filepath: str) -> list[str]:
    """
    Read and return the header list from the first row of a CSV file.

    - Strips leading/trailing whitespace from each header token.
    - Handles Windows (\\r\\n) and Unix (\\n) line endings.

    Raises:
        FileNotFoundError: if the file does not exist.
        ValueError: if the file is empty or the header row has no valid tokens.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, "r", encoding="utf-8", newline="") as fh:
        first_line = fh.readline()

    # Strip universal newline characters
    first_line = first_line.rstrip("\r\n")

    if not first_line.strip():
        raise ValueError(f"File is empty or header row is blank: {filepath}")

    headers = [h.strip() for h in first_line.split(",")]
    headers = [h for h in headers if h]   # drop blank tokens

    if not headers:
        raise ValueError(f"Header row contains no valid headers: {filepath}")

    return headers


def compare_headers(expected: list[str], actual: list[str]) -> dict:
    """
    Compare two header lists and return a structured result dict.

    Returns a dict with keys:
        only_in_expected  : list of headers exclusive to expected
        only_in_actual    : list of headers exclusive to actual
        common            : list of headers present in both
        same_relative_order: bool — True if common headers appear in the
                             same relative order in both files
    """
    expected_set = set(expected)
    actual_set = set(actual)

    only_in_expected = [h for h in expected if h not in actual_set]
    only_in_actual = [h for h in actual if h not in expected_set]
    common = [h for h in expected if h in actual_set]

    # Relative order check: extract common headers in their original positions
    common_in_expected = [h for h in expected if h in set(common)]
    common_in_actual = [h for h in actual if h in set(common)]
    same_relative_order = common_in_expected == common_in_actual

    return {
        "only_in_expected": only_in_expected,
        "only_in_actual": only_in_actual,
        "common": common,
        "same_relative_order": same_relative_order,
    }


# ──────────────────────────────────────────────
# Output formatter
# ──────────────────────────────────────────────

def print_results(expected_path: str, actual_path: str, result: dict) -> None:
    """Pretty-print the comparison results to stdout."""
    sep = "-" * 50

    print(sep)
    print(f"CSV Header Comparison")
    print(f"  Expected : {expected_path}")
    print(f"  Actual   : {actual_path}")
    print(sep)

    print(f"\nOnly in {os.path.basename(expected_path)}:")
    if result["only_in_expected"]:
        for h in result["only_in_expected"]:
            print(f"  {h}")
    else:
        print("  (none)")

    print(f"\nOnly in {os.path.basename(actual_path)}:")
    if result["only_in_actual"]:
        for h in result["only_in_actual"]:
            print(f"  {h}")
    else:
        print("  (none)")

    print("\nCommon headers:")
    if result["common"]:
        for h in result["common"]:
            print(f"  {h}")
    else:
        print("  (none)")

    print(f"\nCommon headers in same relative order: {str(result['same_relative_order']).lower()}")
    print(sep)


# ──────────────────────────────────────────────
# CLI entry point
# ──────────────────────────────────────────────

def main():
    if len(sys.argv) != 3:
        print("Usage: python compare_headers.py <expected_csv> <actual_csv>")
        print("Example: python compare_headers.py expected_orders.csv actual_orders.csv")
        sys.exit(1)

    expected_path = sys.argv[1]
    actual_path = sys.argv[2]

    try:
        expected_headers = read_headers(expected_path)
        actual_headers = read_headers(actual_path)
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)

    result = compare_headers(expected_headers, actual_headers)
    print_results(expected_path, actual_path, result)


if __name__ == "__main__":
    main()
