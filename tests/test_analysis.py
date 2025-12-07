"""Tests for analysis and categorization functions."""

import pytest
import pandas as pd
from smart_parser.categorize import canonicalize_merchant, map_merchant_to_category, add_categories
from smart_parser.analysis import compute_spending_by_category, get_top_spending_category


class TestCanonicalizeMerchant:
    """Test merchant canonicalization."""
    
    def test_uppercase(self):
        """Test that merchant names are uppercased"""
        assert canonicalize_merchant("uber") == "UBER"
        assert canonicalize_merchant("Starbucks") == "STARBUCKS"
    
    def test_whitespace_normalization(self):
        """Test that whitespace is normalized"""
        assert canonicalize_merchant("UBER  *TRIP") == "UBER *TRIP"
        assert canonicalize_merchant("  STARBUCKS  123  ") == "STARBUCKS 123"
    
    def test_none_input(self):
        """Test that None input returns UNKNOWN"""
        assert canonicalize_merchant(None) == "UNKNOWN"
    
    def test_empty_string(self):
        """Test that empty string returns UNKNOWN"""
        assert canonicalize_merchant("") == "UNKNOWN"


class TestMapMerchantToCategory:
    """Test merchant to category mapping."""
    
    def test_uber_transport(self):
        """Test that UBER variants map to Transport"""
        assert map_merchant_to_category("UBER *TRIP") == "Transport"
        assert map_merchant_to_category("Uber Technologies") == "Transport"
        assert map_merchant_to_category("UBER EATS") == "Transport"
    
    def test_lyft_transport(self):
        """Test that LYFT maps to Transport"""
        assert map_merchant_to_category("LYFT *RIDE") == "Transport"
        assert map_merchant_to_category("Lyft Inc") == "Transport"
    
    def test_starbucks_coffee(self):
        """Test that Starbucks maps to Coffee"""
        assert map_merchant_to_category("STARBUCKS 123") == "Coffee"
        assert map_merchant_to_category("Starbucks Coffee") == "Coffee"
    
    def test_dunkin_coffee(self):
        """Test that Dunkin maps to Coffee"""
        assert map_merchant_to_category("DUNKIN DONUTS") == "Coffee"
        assert map_merchant_to_category("Dunkin") == "Coffee"
    
    def test_amazon_shopping(self):
        """Test that Amazon maps to Shopping"""
        assert map_merchant_to_category("Amazon Marketplace") == "Shopping"
        assert map_merchant_to_category("AMZN Mktp US") == "Shopping"
    
    def test_walmart_shopping(self):
        """Test that Walmart maps to Shopping"""
        assert map_merchant_to_category("WALMART SUPERSTORE") == "Shopping"
        assert map_merchant_to_category("Walmart") == "Shopping"
    
    def test_rent_housing(self):
        """Test that rent maps to Housing"""
        assert map_merchant_to_category("RENT PAYMENT") == "Housing"
        assert map_merchant_to_category("Rent Payment") == "Housing"
    
    def test_netflix_entertainment(self):
        """Test that Netflix maps to Entertainment"""
        assert map_merchant_to_category("NETFLIX SUBSCRIPTION") == "Entertainment"
        assert map_merchant_to_category("Netflix") == "Entertainment"
    
    def test_unknown_other(self):
        """Test that unknown merchants map to Other"""
        assert map_merchant_to_category("UNKNOWN MERCHANT") == "Other"
        assert map_merchant_to_category("Random Store") == "Other"


class TestAddCategories:
    """Test adding categories to DataFrame."""
    
    def test_add_categories(self):
        """Test that categories are added correctly"""
        df = pd.DataFrame({
            'merchant': ['UBER *TRIP', 'STARBUCKS 123', 'Amazon Marketplace'],
            'amount': [10.0, 5.0, 100.0]
        })
        
        result = add_categories(df)
        
        assert 'merchant_canonical' in result.columns
        assert 'category' in result.columns
        assert result.loc[0, 'category'] == 'Transport'
        assert result.loc[1, 'category'] == 'Coffee'
        assert result.loc[2, 'category'] == 'Shopping'


class TestComputeSpendingByCategory:
    """Test spending computation by category."""
    
    def test_compute_spending(self):
        """Test spending computation with absolute values"""
        df = pd.DataFrame({
            'category': ['Transport', 'Transport', 'Coffee', 'Coffee'],
            'amount': [10.0, -5.0, 3.0, 2.0]
        })
        
        spending = compute_spending_by_category(df)
        
        assert spending['Transport'] == 15.0  # abs(10) + abs(-5)
        assert spending['Coffee'] == 5.0  # abs(3) + abs(2)
    
    def test_empty_dataframe(self):
        """Test with empty DataFrame"""
        df = pd.DataFrame(columns=['category', 'amount'])
        spending = compute_spending_by_category(df)
        assert spending == {}


class TestGetTopSpendingCategory:
    """Test top spending category identification."""
    
    def test_get_top_category(self):
        """Test that top category is identified correctly"""
        df = pd.DataFrame({
            'category': ['Transport', 'Transport', 'Coffee', 'Shopping'],
            'amount': [10.0, 5.0, 3.0, 100.0]
        })
        
        top = get_top_spending_category(df)
        
        assert top is not None
        assert top[0] == 'Shopping'
        assert top[1] == 100.0
    
    def test_empty_dataframe(self):
        """Test with empty DataFrame"""
        df = pd.DataFrame(columns=['category', 'amount'])
        top = get_top_spending_category(df)
        assert top is None


class TestIntegration:
    """Integration test for the full pipeline."""
    
    def test_full_pipeline(self):
        """Test the full normalization and analysis pipeline"""
        # Create a small synthetic dataset
        df = pd.DataFrame({
            'date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04'],
            'merchant': ['UBER *TRIP', 'STARBUCKS 123', 'Amazon Marketplace', 'RENT PAYMENT'],
            'amount': ['$10.00', '5.00 USD', '$50.00', '$1200.00']
        })
        
        # Normalize
        from smart_parser.normalize import normalize_dataframe
        df_normalized = normalize_dataframe(df)
        
        # Add categories
        df_with_categories = add_categories(df_normalized)
        
        # Get top category
        top = get_top_spending_category(df_with_categories)
        
        # Verify results
        assert top is not None
        assert top[0] == 'Housing'  # $1200.00 should be the top
        assert top[1] == 1200.0
        
        # Verify all categories are present
        spending = compute_spending_by_category(df_with_categories)
        assert 'Transport' in spending
        assert 'Coffee' in spending
        assert 'Shopping' in spending
        assert 'Housing' in spending

