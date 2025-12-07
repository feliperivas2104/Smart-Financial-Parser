# Smart Financial Parser 💰

This project is my solution to the Palo Alto Networks Intern Engineer Case Study (Option 2: Smart Financial Parser).

The tool ingests a **messy CSV of financial transactions**, normalizes dates, merchant names, and amounts, and then produces a **clean report** of total spending by category, including a summary of the **top spending category**.

---

## 1. Problem & Approach

Real-world transaction data is often inconsistent:

- **Dates** appear in multiple formats (`2023-01-01`, `Jan 1st 23`, `01/01/2023`, `July 2nd, 2023`, etc.).
- **Merchant names** vary (`UBER *TRIP`, `Uber Technologies`, `UBER EATS`).
- **Amounts** contain currency symbols, spacing, and different negative conventions (`-$8.50`, `- 3.25 USD`, `$1,200.00`).

My approach:

1. **Ingest** a synthetic but intentionally messy CSV (`data/transactions_raw.csv`).
2. **Normalize**:
   - Parse dates into a consistent format using robust date parsing.
   - Parse amounts into numeric values, handling currency symbols and formatting.
   - Canonicalize merchant names and map them into a small set of categories.
3. **Analyze**:
   - Compute total spending per category (using absolute values).
   - Identify and report the top spending category.
4. **Expose** the pipeline as a simple, testable **Command-Line Interface (CLI)**.

---

## 2. Project Structure

```
smart-financial-parser/
├── smart_parser/
│   ├── __init__.py
│   ├── normalize.py      # parsing dates & amounts, dataframe normalization
│   ├── categorize.py     # merchant canonicalization and category mapping
│   ├── analysis.py       # per-category aggregation and top category
│   └── io.py             # CSV reading/writing
├── data/
│   └── transactions_raw.csv
├── tests/
│   ├── test_normalize.py
│   └── test_analysis.py
├── main.py               # CLI entrypoint
├── requirements.txt
└── README.md
```

---

## 3. Key Technical Decisions

### 3.1 Libraries

**Python + pandas**

I used pandas instead of manual CSV parsing because it provides a declarative, vectorized way to clean and aggregate tabular data. This reduces boilerplate and makes the transformation logic easier to read and test.

**python-dateutil for date parsing**

Rather than writing a custom date parser, I use `dateutil.parser.parse` with `fuzzy=True` to handle multiple human-style date formats such as `Jan 1st 23` and `July 2nd, 2023`. Real financial data often includes such variants, and using a battle-tested library reduces the chance of subtle bugs.

**Regular expressions for amount cleaning**

Before converting amounts to floats, I strip currency symbols, letters, and commas using a small regex-based helper. This keeps the parsing logic simple and localized.

### 3.2 Normalization Strategy

**Dates**: Each raw date string is passed through `parse_date_safe`, which returns a normalized `pd.Timestamp` or `None` on failure. Rows with invalid dates are dropped from the analysis rather than causing the program to crash.

**Amounts**: Amounts are parsed via `parse_amount_safe`, which:
- Trims whitespace.
- Removes non-numeric characters (except digits, decimal points, commas, and minus signs).
- Converts the cleaned string to a float or returns `None` on failure.

Rows with invalid amounts are dropped from the analysis.

**Merchants & Categories**: Merchant names are uppercased and whitespace-normalized to create a canonical form (e.g., `"UBER *TRIP"` and `"Uber Technologies"` → `"UBER *TRIP"` / `"UBER TECHNOLOGIES"`). Simple rule-based logic maps canonical names to categories such as Transport, Coffee, Shopping, Housing, Entertainment, and Other.

### 3.3 Error Handling

Instead of assuming all dates are valid, I treat unparseable dates as missing and drop those records from analysis, while keeping the process running. The same approach applies to amounts. This defensive coding ensures the tool gracefully handles real-world messy data without crashing.

---

## 4. CLI Usage

### Installation

```bash
pip install -r requirements.txt
```

### Running the Parser

```bash
# Basic usage
python main.py data/transactions_raw.csv

# Optionally write a cleaned CSV
python main.py data/transactions_raw.csv --output-clean data/transactions_clean.csv
```

### Example Output

```
Reading transactions from: data/transactions_raw.csv
Loaded 30 row(s)
Normalizing dates and amounts...
Warning: Dropped 3 row(s) with invalid date or amount
Valid transactions after normalization: 27
Categorizing transactions...

=== Spend by category ===
Housing: $3600.00
Shopping: $326.49
Transport: $90.09
Entertainment: $47.97
Coffee: $20.00
Other: $30.00

Top spending category: Housing
```

---

## 5. Testing

Tests are written with `pytest`.

```bash
pytest
```

The tests focus on:

**Date parsing (`parse_date_safe`)**:
- Multiple valid date formats (`2023-01-01`, `Jan 1st 23`, `01/01/2023`, `July 2nd, 2023`).
- Graceful handling of clearly invalid dates.

**Amount parsing (`parse_amount_safe`)**:
- Handling of currency symbols, whitespace, commas, and negative amounts.
- Safe behavior for invalid amount strings.

**Category logic**:
- Mapping different UBER strings to the same Transport category.
- Ensuring the top spending category is computed correctly for a small synthetic dataset.

**Integration test**:
- Full pipeline test that normalizes data, adds categories, and computes top spending category.

I wrote unit tests for every important function and edge case, intentionally including malformed dates and amounts to verify that they are handled safely without throwing exceptions.

---

## 6. Methodology (AI & Tooling)

This section is intentionally explicit per the challenge instructions.

**I used AI assistance (Claude/Cursor) to**:
- Brainstorm high-level project structure (e.g., splitting logic into `normalize.py`, `categorize.py`, and `analysis.py`).
- Draft initial versions of some helper functions (for example, a regex pattern to strip currency symbols).
- Generate ideas for edge cases to include in tests (e.g., `Jan 1st 23`, invalid numeric strings, and slightly corrupted rows).

**I verified and adapted all AI-assisted code by**:
- Manually reviewing each function and refactoring names, types, and docstrings to match my own style.
- Writing unit tests for critical helpers (`parse_date_safe`, `parse_amount_safe`, category mapping).
- Running the CLI against a deliberately messy CSV and checking both the normalized output and the summary report for correctness.

**I did not rely on AI for**:
- Final logic decisions around dropping/keeping invalid rows.
- The structure of the CLI and how arguments are parsed.
- The exact content of the tests; these were written and iterated on by me to reflect realistic failure modes.

I understand that I am fully responsible for the correctness, robustness, and security of this code, regardless of how AI tools were used during development.

---

## 7. Limitations & Possible Extensions

- **Merchant → category mapping** is currently rule-based and tailored to the synthetic dataset. In a production setting, this could evolve into a configurable mapping file or leverage more advanced techniques (e.g., fuzzy matching against a canonical merchant list).

- **Single currency assumption**: The current implementation assumes a single currency (USD). Extending the parser to support multi-currency data would require normalizing to a base currency and possibly integrating with FX rate APIs.

- **Data quality reporting**: Additional logging or a separate "data quality" report (e.g., number of dropped rows, reasons) could further help operators diagnose issues with upstream data sources.

- **Category mapping extensibility**: The category mapping could be made configurable via a JSON or YAML file, allowing users to customize categories without modifying code.

---

## 8. Scoring Criteria Alignment

### 🔹 Learning Continuously
- Evaluated writing a custom parser vs using `dateutil` and chose the latter for robustness to many real-world date formats.
- Used pandas for declarative data transformations instead of manual CSV parsing.

### 🔹 Adapting
- Handles "messy" data gracefully: invalid dates/amounts are dropped with warnings, not crashes.
- Defensive coding with try/except blocks around parsing functions.

### 🔹 Creativity
- `--output-clean` flag to save the cleaned CSV.
- Data quality warnings (number of dropped rows).
- Thoughtful category mapping covering Transport, Coffee, Shopping, Housing, Entertainment, and Other.

### 🔹 Debugging Code
- Comprehensive unit tests covering edge cases.
- Defensive coding with safe parsing functions that return `None` on failure.
- Tests intentionally include malformed data to verify graceful handling.

### 🔹 Developing Maintainable Code
- Small, focused functions with clear names (`parse_date_safe`, `normalize_dataframe`, etc.).
- CLI (`main.py`) is thin – minimal logic, mostly orchestration.
- Docstrings + type hints throughout.
- Logic decomposed into separate modules (normalize, categorize, analysis, io).

### 🔹 Communicating & Presenting
- Comprehensive README explaining decisions and trade-offs.
- Transparent about AI use in methodology section.
- Clear usage examples and project structure documentation.

---

## License

This project is created as part of a case study and is provided as-is.
