"""Tests for normalization functions."""

import pytest
import pandas as pd
from smart_parser.normalize import parse_date_safe, parse_amount_safe, normalize_dataframe


class TestParseDateSafe:
    """Test date parsing with various formats."""
    
    def test_iso_format(self):
        """Test ISO date format: 2023-01-01"""
        result = parse_date_safe("2023-01-01")
        assert result is not None
        assert result.year == 2023
        assert result.month == 1
        assert result.day == 1
    
    def test_us_format(self):
        """Test US date format: 01/01/2023"""
        result = parse_date_safe("01/01/2023")
        assert result is not None
        assert result.year == 2023
        assert result.month == 1
        assert result.day == 1
    
    def test_human_readable_format_1(self):
        """Test human-readable format: Jan 1st 23"""
        result = parse_date_safe("Jan 1st 23")
        assert result is not None
        assert result.year == 2023
        assert result.month == 1
        assert result.day == 1
    
    def test_human_readable_format_2(self):
        """Test human-readable format: July 2nd, 2023"""
        result = parse_date_safe("July 2nd, 2023")
        assert result is not None
        assert result.year == 2023
        assert result.month == 7
        assert result.day == 2
    
    def test_another_format(self):
        """Test another format: 2023/03/05"""
        result = parse_date_safe("2023/03/05")
        assert result is not None
        assert result.year == 2023
        assert result.month == 3
        assert result.day == 5
    
    def test_invalid_date(self):
        """Test that invalid dates return None gracefully"""
        result = parse_date_safe("INVALID DATE")
        assert result is None
    
    def test_none_input(self):
        """Test that None input returns None"""
        assert parse_date_safe(None) is None
    
    def test_empty_string(self):
        """Test that empty string returns None"""
        assert parse_date_safe("") is None
        assert parse_date_safe("   ") is None


class TestParseAmountSafe:
    """Test amount parsing with various formats."""
    
    def test_currency_symbol(self):
        """Test amount with dollar sign: $12.34"""
        result = parse_amount_safe("$12.34")
        assert result == 12.34
    
    def test_currency_code(self):
        """Test amount with currency code: 15.00 USD"""
        result = parse_amount_safe("15.00 USD")
        assert result == 15.00
    
    def test_negative_with_symbol(self):
        """Test negative amount: -$8.50"""
        result = parse_amount_safe("-$8.50")
        assert result == -8.50
    
    def test_negative_with_space(self):
        """Test negative amount with space: - 3.25 USD"""
        result = parse_amount_safe("- 3.25 USD")
        assert result == -3.25
    
    def test_with_commas(self):
        """Test amount with thousand separators: $1,200.00"""
        result = parse_amount_safe("$1,200.00")
        assert result == 1200.00
    
    def test_with_whitespace(self):
        """Test amount with whitespace: $ 12.34"""
        result = parse_amount_safe("$ 12.34")
        assert result == 12.34
    
    def test_numeric_input(self):
        """Test that numeric input is handled"""
        assert parse_amount_safe(12.34) == 12.34
        assert parse_amount_safe(100) == 100.0
        assert parse_amount_safe(-50) == -50.0
    
    def test_invalid_amount(self):
        """Test that invalid amounts return None gracefully"""
        assert parse_amount_safe("NOT_A_NUMBER") is None
        assert parse_amount_safe("INVALID AMOUNT") is None
    
    def test_none_input(self):
        """Test that None input returns None"""
        assert parse_amount_safe(None) is None
    
    def test_empty_string(self):
        """Test that empty string returns None"""
        assert parse_amount_safe("") is None
        assert parse_amount_safe("   ") is None


class TestNormalizeDataframe:
    """Test DataFrame normalization."""
    
    def test_normalize_valid_data(self):
        """Test normalization with valid data"""
        df = pd.DataFrame({
            'date': ['2023-01-01', '2023-02-15'],
            'merchant': ['UBER', 'STARBUCKS'],
            'amount': ['$12.34', '15.00 USD']
        })
        
        result = normalize_dataframe(df)
        
        assert len(result) == 2
        assert pd.api.types.is_datetime64_any_dtype(result['date'])
        assert pd.api.types.is_numeric_dtype(result['amount'])
    
    def test_normalize_drops_invalid_rows(self):
        """Test that invalid rows are dropped"""
        df = pd.DataFrame({
            'date': ['2023-01-01', 'INVALID DATE', '2023-02-15'],
            'merchant': ['UBER', 'MERCHANT', 'STARBUCKS'],
            'amount': ['$12.34', 'NOT_A_NUMBER', '15.00 USD']
        })
        
        result = normalize_dataframe(df)
        
        # Should only have 2 valid rows
        assert len(result) == 2
        assert all(result['date'].notna())
        assert all(result['amount'].notna())
    
    def test_normalize_empty_dataframe(self):
        """Test normalization with empty DataFrame"""
        df = pd.DataFrame(columns=['date', 'merchant', 'amount'])
        result = normalize_dataframe(df)
        assert len(result) == 0

