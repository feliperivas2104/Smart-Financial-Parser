#!/usr/bin/env python3
"""CLI entrypoint for Smart Financial Parser."""

import argparse
import sys
from pathlib import Path

from smart_parser.io import read_transactions_csv, write_clean_csv
from smart_parser.normalize import normalize_dataframe
from smart_parser.categorize import add_categories
from smart_parser.analysis import print_spending_report


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Normalize and analyze messy financial transaction data"
    )
    parser.add_argument(
        'input_csv',
        type=str,
        help='Path to the messy CSV file with transactions'
    )
    parser.add_argument(
        '--output-clean',
        type=str,
        default=None,
        help='Optional: Path to save the cleaned/normalized CSV'
    )
    
    args = parser.parse_args()
    
    # Read the messy CSV
    try:
        print(f"Reading transactions from: {args.input_csv}")
        df_raw = read_transactions_csv(args.input_csv)
        print(f"Loaded {len(df_raw)} row(s)")
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Normalize dates and amounts
    print("Normalizing dates and amounts...")
    df_normalized = normalize_dataframe(df_raw)
    print(f"Valid transactions after normalization: {len(df_normalized)}")
    
    # Add categories
    print("Categorizing transactions...")
    df_with_categories = add_categories(df_normalized)
    
    # Print analysis report
    print_spending_report(df_with_categories)
    
    # Optionally save cleaned CSV
    if args.output_clean:
        try:
            # Select columns for output (date, merchant_canonical, amount, category)
            output_cols = ['date', 'merchant_canonical', 'amount', 'category']
            df_output = df_with_categories[output_cols].copy()
            
            # Format date for readability
            df_output['date'] = df_output['date'].dt.strftime('%Y-%m-%d')
            
            write_clean_csv(df_output, args.output_clean)
        except Exception as e:
            print(f"Warning: Could not write cleaned CSV: {e}", file=sys.stderr)


if __name__ == '__main__':
    main()

