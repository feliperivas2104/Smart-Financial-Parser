"""Merchant canonicalization and category mapping logic."""

import re
from typing import Optional
import pandas as pd


from typing import Optional

def canonicalize_merchant(merchant: Optional[str]) -> str:
    """
    Canonicalize a merchant name by uppercasing and normalizing whitespace.
    
    Args:
        merchant: Raw merchant name from CSV
        
    Returns:
        Canonicalized merchant name (uppercase, single spaces)
    """
    if merchant is None or not isinstance(merchant, str):
        return "UNKNOWN"
    
    # Uppercase and normalize whitespace
    canonical = re.sub(r'\s+', ' ', merchant.strip().upper())
    return canonical if canonical else "UNKNOWN"


def map_merchant_to_category(merchant: str) -> str:
    """
    Map a canonicalized merchant name to a spending category.
    
    Uses simple rule-based matching. In production, this could be:
    - A configurable mapping file
    - Fuzzy matching against a canonical merchant database
    - Machine learning classification
    
    Args:
        merchant: Canonicalized merchant name
        
    Returns:
        Category name (Transport, Coffee, Shopping, Housing, Other)
    """
    merchant_upper = merchant.upper()
    
    # Transport
    if any(keyword in merchant_upper for keyword in ['UBER', 'LYFT', 'TAXI', 'RIDE']):
        return "Transport"
    
    # Coffee
    if any(keyword in merchant_upper for keyword in ['STARBUCKS', 'DUNKIN', 'COFFEE', 'CAFE']):
        return "Coffee"
    
    # Shopping
    if any(keyword in merchant_upper for keyword in ['AMAZON', 'AMZN', 'WALMART', 'TARGET', 'SHOP']):
        return "Shopping"
    
    # Housing
    if any(keyword in merchant_upper for keyword in ['RENT', 'HOUSING', 'MORTGAGE', 'UTILITY']):
        return "Housing"
    
    # Entertainment
    if any(keyword in merchant_upper for keyword in ['NETFLIX', 'SPOTIFY', 'ENTERTAINMENT']):
        return "Entertainment"
    
    # Default category
    return "Other"


def add_categories(df: pd.DataFrame, merchant_col: str = 'merchant') -> pd.DataFrame:
    """
    Add canonicalized merchant names and categories to a DataFrame.
    
    Args:
        df: DataFrame with merchant column
        merchant_col: Name of the merchant column (default: 'merchant')
        
    Returns:
        DataFrame with added 'merchant_canonical' and 'category' columns
    """
    result = df.copy()
    
    # Canonicalize merchants
    result['merchant_canonical'] = result[merchant_col].apply(canonicalize_merchant)
    
    # Map to categories
    result['category'] = result['merchant_canonical'].apply(map_merchant_to_category)
    
    return result

