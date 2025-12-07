# Smart Financial Parser  
Normalize messy financial transaction data and generate a spending summary via a simple CLI.

This tool ingests intentionally chaotic financial data—including inconsistent dates, varied merchant naming conventions, and messy currency formats—and produces a clean, standardized dataset along with a report identifying top spending categories.

This project is submitted as part of Option 2: **Smart Financial Parser** for the Palo Alto Networks Intern Engineer Challenge.

---

## Features

## Robust CSV ingestion  
- Validates required columns (`date`, `merchant`, `amount`)  
- Clear error messages for missing files or malformed input  

## Normalization of messy real-world data  
- **Date normalization:** Handles ISO, US, human-readable formats, and fuzzy text  
- **Amount normalization:** Cleans currency symbols, text (`USD`), thousand separators, and negative formats  
- Drops invalid rows gracefully with warnings — never crashes  

## Merchant categorization  
Maps canonicalized merchant names into high-level categories using rule-based logic:
- Transport  
- Coffee  
- Shopping  
- Housing  
- Entertainment  
- Other  

## Analysis  
- Computes total spending per category using absolute values  
- Identifies the top spending category  
- Prints a clean, readable spending report  

## Command-Line Interface  
Example:
```bash
python3 main.py data/transactions_raw.csv
python3 main.py data/transactions_raw.csv --output-clean data/cleaned.csv

## 🧠 Methodology (AI Usage Disclosure)

I used AI tools — primarily **Cursor AI** and **ChatGPT** — to assist with drafting parts of the code, generating ideas for handling messy data, and helping structure documentation.

All AI-generated suggestions were **manually reviewed, rewritten, and tested by me**. I refactored the logic, verified behavior against edge cases, and validated everything using the full pytest suite plus manual testing of the CLI.

AI helped accelerate development, but **I take full responsibility for the correctness, safety, and maintainability of the final implementation**. This aligns with Palo Alto Networks’ expectation of using modern tools for leverage while ensuring engineering rigor and ownership.

