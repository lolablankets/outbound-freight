# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development
- **Run Python**: Always use `uv` instead of direct python commands
- **Install dependencies**: `uv add <package>` or `uv sync`
- **Run tests**: `uv run pytest` (runs all tests) or `uv run pytest tests/test_specific.py`
- **Run single test**: `uv run pytest tests/test_vendor_detection.py::test_function_name -v`

### Project Structure
- **Main package**: `outbound_freight/` contains the core Python package
- **Tests**: `tests/` directory with pytest-based test suite
- **Data samples**: `data/2025/08/` contains sample invoice files for testing
- **Documentation**: `docs/` contains schema documentation for vendor invoice formats

## Architecture

This is a Python package for processing shipping invoices from multiple vendors (FedEx, UPS, USPS) to calculate weighted average shipping costs per product.

### Core Components
- **Vendor Detection** (`outbound_freight/vendor_detection.py`): Identifies shipping vendor from filename patterns
  - `Vendor` enum with FEDEX, UPS, USPS, UNKNOWN
  - `detect_vendor()` function uses filename heuristics (fdx/fedex, ups, usps/stamps keywords)

### Data Processing Pipeline
The project follows a 10-step process outlined in README.md:
1. Vendor detection from filenames
2. Dynamic header detection in Excel/CSV files
3. Field cleaning and normalization
4. Schema mapping to common format
5. Data extraction to unified schema
6. Consolidation and deduplication
7. Snowflake data warehouse integration for order data
8. Order matching via tracking codes
9. Quality control and match rate optimization
10. Weighted average cost calculation per product type/size

### Invoice Schema Documentation
- `docs/fedex_schema.md`: FedEx invoice structure and field patterns (154 lines of analysis)
- `docs/ups_schema.md`: UPS invoice structure and field patterns (161 lines of analysis)  
- `docs/usps_schema.md`: USPS schema (placeholder file)
- `docs/analysis_schema.md`: Final output schema (placeholder file)

### Dependencies
- **pandas**: Data manipulation and processing
- **openpyxl**: Excel file reading
- **google-api-python-client**: Google Sheets integration
- **pytest**: Testing framework
- **ipykernel**: Jupyter notebook support for data analysis

### Test Strategy
**IMPORTANT: FOLLOW TEST-DRIVEN DEVELOPMENT (TDD) - WRITE TESTS FIRST, THEN IMPLEMENTATION**

Tests verify vendor detection against both synthetic filenames and actual data samples in the repository. The test suite includes parametrized tests that expect specific sample files to exist in `data/2025/08/`.