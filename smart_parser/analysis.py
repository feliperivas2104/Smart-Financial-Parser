"""Analysis functions for finding spending summaries and top categories."""

from typing import Dict, Tuple
import pandas as pd


def compute_spending_by_category(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate total amount of spending per category using absolute values.
    
    Args:
        DataFrame with 'category' and 'amount' columns
        
    Returns:
        Dictionary mapping category names to total spending (absolute values)
    """
    if df.empty or 'category' not in df.columns or 'amount' not in df.columns:
        return {}
    
    # Use absolute values to handle both debits and credits
    df_copy = df.copy()
    df_copy['amount_abs'] = df_copy['amount'].abs()
    
    # Group by category and sum
    spending = df_copy.groupby('category')['amount_abs'].sum().to_dict()
    
    return spending


from typing import Optional, Tuple

def get_top_spending_category(df: pd.DataFrame) -> Optional[Tuple[str, float]]:
    """
    Identify the top spending category and its total amount.
    
    Args:
        DataFrame with 'category' and 'amount' columns
        
    Returns:
        Tuple of (category_name, total_amount) or None if no data
    """
    spending = compute_spending_by_category(df)
    
    if not spending:
        return None
    
    # Find category with maximum spending
    top_category = max(spending.items(), key=lambda x: x[1])
    return top_category


def print_spending_report(df: pd.DataFrame) -> None:
    """
    Print a formatted spending report to stdout.
    
    Args:
        df: DataFrame with 'category' and 'amount' columns
    """
    spending = compute_spending_by_category(df)
    
    if not spending:
        print("No spending data available.")
        return
    
    print("\n=== Spend by category ===")
    
    # Sort in descending order (easier to read)
    sorted_spending = sorted(spending.items(), key=lambda x: x[1], reverse=True)
    
    for category, amount in sorted_spending:
        print(f"{category}: ${amount:.2f}")
    
    # Print top category
    top = get_top_spending_category(df)
    if top:
        print(f"\nTop spending category: {top[0]}")
    
    print()  # Empty line at end

