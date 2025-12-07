"""Normalization functions for parsing dates and amounts from messy transaction data."""

from datetime import datetime
from typing import Optional
import re
from dateutil import parser as date_parser
import pandas as pd


from typing import Optional

def parse_date_safe(raw: Optional[str]) -> Optional[pd.Timestamp]:
    """
    Parse a messy date string into a normalized Timestamp (or None on failure).
    
    Handles multiple date formats including:
    - ISO format: 2023-01-01
    - US format: 01/01/2023
    - Human-readable: Jan 1st 23, July 2nd, 2023
    - Various other formats via dateutil's fuzzy parsing
    
    Args:
        raw: Raw date string from CSV
        
    Returns:
        pd.Timestamp if parsing succeeds, None otherwise
    """
    if raw is None or not isinstance(raw, str):
        return None
    
    raw = raw.strip()
    if not raw:
        return None
    
    try:
        # Use dateutil's parser with fuzzy=True to handle various formats
        parsed = date_parser.parse(raw, fuzzy=True)
        return pd.Timestamp(parsed)
    except (ValueError, TypeError, OverflowError):
        # Gracefully handle unparseable dates
        return None


from typing import Optional, Union

def parse_amount_safe(raw: Union[str, float, int, None]) -> Optional[float]:
    """
    Parse a messy amount string into a float (or None on failure).
    
    Handles:
    - Currency symbols: $12.34, 15.00 USD
    - Negative amounts: -$8.50, - 3.25 USD
    - Commas: $1,200.00
    - Whitespace: $ 12.34, 15.00 USD
    
    Args:
        raw: Raw amount string or numeric value
        
    Returns:
        float if parsing succeeds, None otherwise
    """
    if raw is None:
        return None
    
    # If already numeric, return as float
    if isinstance(raw, (int, float)):
        return float(raw)
    
    if not isinstance(raw, str):
        return None
    
    raw = raw.strip()
    if not raw:
        return None
    
    try:
        # Remove currency symbols and letters (USD, EUR, etc.)
        # Keep digits, decimal points, commas, and minus signs
        cleaned = re.sub(r'[^\d.,-]', '', raw)
        
        # Remove commas (thousand separators)
        cleaned = cleaned.replace(',', '')
        
        # Handle negative signs that might have spaces
        cleaned = cleaned.replace(' ', '')
        
        if not cleaned or cleaned == '-':
            return None
        
        # Convert to float
        return float(cleaned)
    except (ValueError, TypeError):
        return None


def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize a DataFrame of transactions by parsing dates and amounts.
    
    Drops rows where date or amount cannot be parsed.
    
    Args:
        df: Raw DataFrame with columns: date, merchant, amount
        
    Returns:
        Normalized DataFrame with parsed dates and amounts, invalid rows removed
    """
    if df.empty:
        return df.copy()
    
    # Create a copy to avoid modifying the original
    normalized = df.copy()
    
    # Parse dates
    normalized['date'] = normalized['date'].apply(parse_date_safe)
    
    # Parse amounts
    normalized['amount'] = normalized['amount'].apply(parse_amount_safe)
    
    # Drop rows where date or amount is None (invalid)
    initial_count = len(normalized)
    normalized = normalized.dropna(subset=['date', 'amount'])
    dropped_count = initial_count - len(normalized)
    
    if dropped_count > 0:
        print(f"Warning: Dropped {dropped_count} row(s) with invalid date or amount")
    
    # Ensure date column is datetime type
    normalized['date'] = pd.to_datetime(normalized['date'])
    
    # Reset index after dropping rows
    normalized = normalized.reset_index(drop=True)
    
    return normalized

