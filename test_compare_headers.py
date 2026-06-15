"""
test_compare_headers.py
-----------------------
Unit tests for compare_headers.py

Tests cover:
  1. Identical headers
  2. One header missing in actual
  3. Extra whitespace around headers
  4. Windows line endings (CRLF)
  5. Common headers present but in different order
  6. Empty file error handling
  7. Missing file error handling
  8. Header row with no valid tokens

Run with:
    pytest test_compare_headers.py -v

Author: Anandababu M
"""

import os
import sys
import tempfile
import pytest

# Import the functions we want to test
from compare_headers import read_headers, compare_headers


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def write_temp_csv(content: str, suffix: str = ".csv") -> str:
    """Write content to a temp file and return its path."""
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(content)
    return path


# ──────────────────────────────────────────────
# Tests for read_headers()
# ──────────────────────────────────────────────

class TestReadHeaders:

    def test_standard_headers(self):
        """Normal CSV header row is read correctly."""
        path = write_temp_csv("order_id,customer_id,amount\n1,C001,100.50\n")
        try:
            headers = read_headers(path)
            assert headers == ["order_id", "customer_id", "amount"]
        finally:
            os.unlink(path)

    def test_headers_with_spaces_are_trimmed(self):
        """Whitespace around headers must be stripped."""
        path = write_temp_csv(" order_id , customer_id , amount \n1,C001,100\n")
        try:
            headers = read_headers(path)
            assert headers == ["order_id", "customer_id", "amount"]
        finally:
            os.unlink(path)

    def test_windows_crlf_line_endings(self):
        """Windows-style CRLF endings are handled without \\r in header names."""
        path = write_temp_csv("order_id,customer_id,amount\r\n1,C001,100\r\n")
        try:
            headers = read_headers(path)
            assert "amount" in headers
            assert all("\r" not in h for h in headers), "\\r should be stripped from headers"
        finally:
            os.unlink(path)

    def test_empty_file_raises_value_error(self):
        """Empty file should raise ValueError."""
        path = write_temp_csv("")
        try:
            with pytest.raises(ValueError, match="empty or header row is blank"):
                read_headers(path)
        finally:
            os.unlink(path)

    def test_file_not_found_raises_error(self):
        """Non-existent file path should raise FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            read_headers("/tmp/this_file_does_not_exist_abc123.csv")

    def test_header_row_only_commas_raises_value_error(self):
        """A header row that is only commas/spaces has no valid tokens."""
        path = write_temp_csv("  ,  ,  \n")
        try:
            with pytest.raises(ValueError, match="no valid headers"):
                read_headers(path)
        finally:
            os.unlink(path)


# ──────────────────────────────────────────────
# Tests for compare_headers()
# ──────────────────────────────────────────────

class TestCompareHeaders:

    def test_identical_headers(self):
        """Two files with exactly the same headers."""
        headers = ["order_id", "customer_id", "amount"]
        result = compare_headers(headers, headers)

        assert result["only_in_expected"] == []
        assert result["only_in_actual"] == []
        assert set(result["common"]) == {"order_id", "customer_id", "amount"}
        assert result["same_relative_order"] is True

    def test_one_header_missing_in_actual(self):
        """Actual file is missing one header from expected."""
        expected = ["order_id", "customer_id", "amount", "currency"]
        actual = ["order_id", "customer_id", "currency"]

        result = compare_headers(expected, actual)

        assert result["only_in_expected"] == ["amount"]
        assert result["only_in_actual"] == []
        assert "amount" not in result["common"]
        assert result["same_relative_order"] is True  # remaining common headers in same order

    def test_extra_header_in_actual(self):
        """Actual file introduces a header not in expected."""
        expected = ["order_id", "customer_id"]
        actual = ["order_id", "customer_id", "extra_column"]

        result = compare_headers(expected, actual)

        assert result["only_in_actual"] == ["extra_column"]
        assert result["only_in_expected"] == []

    def test_common_headers_different_order(self):
        """Common headers exist in both files but in different relative order."""
        expected = ["order_id", "customer_id", "amount"]
        actual = ["amount", "customer_id", "order_id"]   # reversed

        result = compare_headers(expected, actual)

        assert set(result["common"]) == {"order_id", "customer_id", "amount"}
        assert result["same_relative_order"] is False

    def test_no_common_headers(self):
        """No headers overlap between the two files."""
        expected = ["col_a", "col_b"]
        actual = ["col_c", "col_d"]

        result = compare_headers(expected, actual)

        assert set(result["only_in_expected"]) == {"col_a", "col_b"}
        assert set(result["only_in_actual"]) == {"col_c", "col_d"}
        assert result["common"] == []
        assert result["same_relative_order"] is True   # vacuously true — nothing to compare

    def test_whitespace_stripped_before_compare(self):
        """Headers with surrounding spaces should match after stripping."""
        expected_path = write_temp_csv(" order_id , customer_id \n")
        actual_path = write_temp_csv("order_id,customer_id\n")
        try:
            expected = read_headers(expected_path)
            actual = read_headers(actual_path)
            result = compare_headers(expected, actual)
            assert result["only_in_expected"] == []
            assert result["only_in_actual"] == []
            assert result["same_relative_order"] is True
        finally:
            os.unlink(expected_path)
            os.unlink(actual_path)
