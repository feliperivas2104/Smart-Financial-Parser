"""I/O functions for reading and writing CSV files."""

import pandas as pd
from pathlib import Path
from typing import Optional


from typing import Union

def read_transactions_csv(file_path: Union[str, Path]) -> pd.DataFrame:
    """
    Read a CSV file of transactions.
    
    Expected columns: date, merchant, amount
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        DataFrame with transaction data
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")
    
    try:
        df = pd.read_csv(file_path)
        
        # Validate required columns
        required_cols = ['date', 'merchant', 'amount']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        return df
    except pd.errors.EmptyDataError:
        raise ValueError(f"CSV file is empty: {file_path}")
    except Exception as e:
        raise RuntimeError(f"Error reading CSV file: {e}")


from typing import Union  # already at the top

def write_clean_csv(df: pd.DataFrame, file_path: Union[str, Path]) -> None:
    """
    Write a cleaned DataFrame to a CSV file.
    
    Args:
        df: DataFrame to write
        file_path: Path where the CSV should be written
    """
    file_path = Path(file_path)
    
    # Create parent directory if it doesn't exist
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        df.to_csv(file_path, index=False)
        print(f"Cleaned data written to: {file_path}")
    except Exception as e:
        raise RuntimeError(f"Error writing CSV file: {e}")

