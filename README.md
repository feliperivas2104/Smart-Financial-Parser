# Smart Financial Parser  
Normalize messy financial transaction data and generate a spending summary via a simple CLI.

This tool gets a chaotic financial data, which includes: inconsistent dates, different types of names for things purchased, and differing currency formats. It then produces anorganized dataset along with a report identifying top spending categories.

This project is submitted as Option 2: **Smart Financial Parser**.

---

## Features

## Robust CSV ingestion  
- Validates required columns (`date`, `merchant`, `amount`)  
- Clear error messages for missing files or malformed input  
- Outputs something as other if it doesn't fit within a category

## Normalization of messy real-world data  
- **Date normalization:** Handles different formats and fuzzy text  
- **Amount normalization:** Cleans currency symbols, text (`USD`), and negative numbers  
- Drops invalid rows with warnings — never crashes  

## Merchant categorization  
Maps canonicalized merchant names into categories using  simple logic:
- Transport  
- Coffee  
- Shopping  
- Housing  
- Entertainment  
- Other  

## Analysis  
- Computes total spending per category using absolute values  
- Identifies the top spending category  
- Prints a clean spending report in descending order.

## Command-Line Interface  
Example:
```bash
python3 main.py data/transactions_raw.csv
python3 main.py data/transactions_raw.csv --output-clean data/cleaned.csv
```

## Methodology AI Usage

I used AI tools (ChatGPT) to assist with drafting parts of the code, to help structure documentation, to help me with the test cases since it has been a while since i've done them, and to generate a list of dummy data to actually test what was being output.

I reviewed all the ai suggestions presented to me and I verified behavior with every edge case.


