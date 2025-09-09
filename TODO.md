# TODO: Outbound Freight Invoice Processing Pipeline

## Overview
Process shipping invoices from FedEx, UPS, and USPS to calculate weighted average shipping costs per product. Follow **TEST-DRIVEN DEVELOPMENT (TDD)** - write tests first, then implementation.

---

## PHASE 1: VENDOR DETECTION & FILE READING

### 1.1 Vendor Detection from Filenames
**Test Requirements:**
- [ ] Write test for FedEx detection: files containing 'fdx', 'fedex' (case insensitive)
- [ ] Write test for UPS detection: files containing 'ups' (case insensitive)  
- [ ] Write test for USPS detection: files containing 'usps', 'stamps' (case insensitive)
- [ ] Write test for unknown vendor fallback
- [ ] Write test against actual sample files in `data/2025/08/`

**Implementation Requirements:**
- [ ] Implement robust vendor detection function
- [ ] Handle edge cases (multiple vendor keywords, special characters)
- [ ] Return appropriate Vendor enum values

**Acceptance Criteria:**
- 100% of test sample files correctly identified
- Function handles malformed filenames gracefully

**Quality Gate:** All vendor detection tests pass with 100% accuracy on sample data

---

### 1.2 File Reading & Format Detection  
**Test Requirements:**
- [ ] Write test for Excel (.xlsx) file reading
- [ ] Write test for CSV file reading
- [ ] Write test for malformed/corrupted file handling
- [ ] Write test for empty file handling

**Implementation Requirements:**
- [ ] Create unified file reader that handles both Excel and CSV
- [ ] Implement proper error handling and logging
- [ ] Support for different encodings (UTF-8, Windows-1252, etc.)

**Acceptance Criteria:**
- Successfully reads all sample invoice files
- Graceful error handling for corrupted files

**Quality Gate:** File reader handles 100% of sample files without errors

---

## PHASE 2: DYNAMIC HEADER DETECTION

### 2.1 Header Row Detection
**Test Requirements:**
- [ ] Write test for headers in row 1 (standard case)
- [ ] Write test for headers in rows 2-10 (common cases)  
- [ ] Write test for headers with merged cells
- [ ] Write test for headers with special characters/formatting
- [ ] Write test for missing headers (error case)
- [ ] Write test against each vendor's actual sample files

**Implementation Requirements:**
- [ ] Implement dynamic header detection algorithm
- [ ] Handle merged cells and formatting
- [ ] Detect headers based on content patterns (not just position)
- [ ] Support vendor-specific header patterns

**Acceptance Criteria:**
- Correctly identifies header row in 95% of test cases
- Handles edge cases (empty rows, merged cells) gracefully
- Returns structured header mapping with confidence scores

**Quality Gate:** Header detection accuracy ≥95% across all sample files

---

### 2.2 Header Validation & Mapping
**Test Requirements:**
- [ ] Write test for required field presence validation
- [ ] Write test for header name normalization
- [ ] Write test for vendor-specific header variations
- [ ] Write test for duplicate header handling

**Implementation Requirements:**  
- [ ] Validate presence of critical fields per vendor
- [ ] Normalize header names (lowercase, underscores)
- [ ] Create vendor-specific header mapping dictionaries
- [ ] Handle duplicate or similar header names

**Acceptance Criteria:**
- Identifies all required fields for each vendor type
- Normalizes headers consistently across vendors
- Provides clear error messages for missing critical fields

**Quality Gate:** All sample files pass header validation with normalized field names

---

## PHASE 3: FIELD CLEANING & NORMALIZATION

### 3.1 Currency Field Cleaning
**Test Requirements:**
- [ ] Write test for dollar sign removal: "$38.33" → 38.33
- [ ] Write test for comma removal: "$1,234.56" → 1234.56
- [ ] Write test for parentheses (negative): "($38.33)" → -38.33
- [ ] Write test for currency symbols: "€123.45", "£98.76"
- [ ] Write test for malformed currency strings
- [ ] Write test for null/empty values

**Implementation Requirements:**
- [ ] Implement robust currency string parser
- [ ] Handle multiple currency formats
- [ ] Preserve precision for decimal values
- [ ] Handle edge cases and invalid formats

**Acceptance Criteria:**
- Converts 100% of valid currency strings correctly
- Handles invalid formats gracefully with appropriate errors
- Maintains precision to 2 decimal places

**Quality Gate:** Currency cleaning function passes all test cases with 100% accuracy

---

### 3.2 Date Field Cleaning  
**Test Requirements:**
- [ ] Write test for standard format: "7/31/2025 12:00:00 AM"
- [ ] Write test for various date formats: "MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD"
- [ ] Write test for date-only strings: "7/31/2025"
- [ ] Write test for malformed dates
- [ ] Write test for timezone handling
- [ ] Write test for null/empty date values

**Implementation Requirements:**
- [ ] Implement flexible date parser supporting multiple formats
- [ ] Handle ambiguous date formats consistently
- [ ] Convert all dates to standard datetime objects
- [ ] Preserve timezone information when available

**Acceptance Criteria:**
- Parses 95% of date strings correctly
- Consistent handling of ambiguous formats (MM/DD vs DD/MM)
- Returns standardized datetime objects

**Quality Gate:** Date parsing accuracy ≥95% across all sample data

---

### 3.3 Text Field Normalization
**Test Requirements:**
- [ ] Write test for field name normalization: "Customer Name" → "customer_name"
- [ ] Write test for whitespace trimming and standardization
- [ ] Write test for special character handling
- [ ] Write test for encoding issues (UTF-8, Windows-1252)

**Implementation Requirements:**
- [ ] Implement text normalization utilities
- [ ] Handle various encodings consistently
- [ ] Standardize whitespace and special characters
- [ ] Preserve important formatting where needed

**Acceptance Criteria:**
- Consistent field name formatting across all vendors
- Proper handling of special characters and encodings
- No data loss during normalization

**Quality Gate:** All text fields normalized consistently without data corruption

---

## PHASE 4: SCHEMA MAPPING & FIELD MAPPING

### 4.1 Common Schema Definition
**Test Requirements:**
- [ ] Write test validating common schema structure
- [ ] Write test for required vs optional field definitions
- [ ] Write test for data type specifications
- [ ] Write test for field validation rules

**Implementation Requirements:**
- [ ] Define comprehensive common schema for all vendors
- [ ] Specify required vs optional fields
- [ ] Define data types and validation rules
- [ ] Include metadata fields (vendor, processing_date, etc.)

**Acceptance Criteria:**
- Schema covers all critical invoice data points
- Clear distinction between required and optional fields
- Extensible for future vendor additions

**Quality Gate:** Schema definition complete and documented

---

### 4.2 FedEx Field Mapping
**Test Requirements:**
- [ ] Write test mapping FedEx headers to common schema
- [ ] Write test for FedEx-specific field variations
- [ ] Write test against actual FedEx sample files
- [ ] Write test for missing field handling

**Implementation Requirements:**
- [ ] Create comprehensive FedEx field mapping dictionary
- [ ] Handle multiple possible names for each common field
- [ ] Implement FedEx-specific business logic
- [ ] Support schema evolution over time

**Acceptance Criteria:**
- Maps all critical FedEx fields to common schema
- Handles field name variations robustly
- Processes all FedEx sample files successfully

**Quality Gate:** 100% of FedEx sample files successfully mapped to common schema

---

### 4.3 UPS Field Mapping
**Test Requirements:**
- [ ] Write test mapping UPS headers to common schema
- [ ] Write test for UPS-specific field variations
- [ ] Write test against actual UPS sample files  
- [ ] Write test for missing field handling

**Implementation Requirements:**
- [ ] Create comprehensive UPS field mapping dictionary
- [ ] Handle multiple possible names for each common field
- [ ] Implement UPS-specific business logic
- [ ] Support schema evolution over time

**Acceptance Criteria:**
- Maps all critical UPS fields to common schema
- Handles field name variations robustly  
- Processes all UPS sample files successfully

**Quality Gate:** 100% of UPS sample files successfully mapped to common schema

---

### 4.4 USPS Field Mapping
**Test Requirements:**
- [ ] Write test mapping USPS headers to common schema
- [ ] Write test for USPS-specific field variations
- [ ] Write test against actual USPS sample files
- [ ] Write test for missing field handling

**Implementation Requirements:**
- [ ] Create comprehensive USPS field mapping dictionary
- [ ] Handle multiple possible names for each common field
- [ ] Implement USPS-specific business logic  
- [ ] Support schema evolution over time

**Acceptance Criteria:**
- Maps all critical USPS fields to common schema
- Handles field name variations robustly
- Processes all USPS sample files successfully

**Quality Gate:** 100% of USPS sample files successfully mapped to common schema

---

## PHASE 5: DATA EXTRACTION TO UNIFIED SCHEMA

### 5.1 Data Extraction Engine
**Test Requirements:**
- [ ] Write test for successful data extraction from each vendor
- [ ] Write test for data type validation during extraction
- [ ] Write test for handling missing/null values

**Implementation Requirements:**
- [ ] Implement unified data extraction engine
- [ ] Apply field mappings and cleaning functions
- [ ] Validate data types and constraints
- [ ] Handle missing data appropriately

**Acceptance Criteria:**
- Extracts data from all vendor formats successfully
- Validates data integrity during extraction

**Quality Gate:** All sample files successfully extracted with data validation passing

---

### 5.2 Data Quality Validation
**Test Requirements:**
- [ ] Write test for required field presence validation
- [ ] Write test for data type validation
- [ ] Write test for business rule validation (e.g., positive amounts)
- [ ] Write test for duplicate record detection
- [ ] Write test for data completeness scoring

**Implementation Requirements:**
- [ ] Implement comprehensive data quality checks
- [ ] Validate business rules and constraints
- [ ] Generate data quality reports
- [ ] Flag suspicious or invalid records

**Acceptance Criteria:**
- Comprehensive validation of all extracted data
- Clear quality scores and error reporting
- Automated flagging of data issues

**Quality Gate:** Data quality validation passes with >95% clean records

---

## PHASE 6: CONSOLIDATION & DEDUPLICATION

### 6.1 Data Consolidation
**Test Requirements:**
- [ ] Write test for combining data from multiple files
- [ ] Write test for handling overlapping time periods
- [ ] Write test for vendor-specific consolidation logic

**Implementation Requirements:**
- [ ] Implement data consolidation pipeline
- [ ] Handle overlapping data gracefully
- [ ] Maintain data lineage and source tracking
- [ ] Optimize for large datasets

**Acceptance Criteria:**
- Successfully consolidates data from all vendors
- Preserves data lineage and source information
- Handles overlapping periods without duplication

**Quality Gate:** Consolidated dataset contains all unique records with proper source tracking

---

### 6.2 Deduplication Logic
**Test Requirements:**
- [ ] Write test for exact duplicate detection
- [ ] Write test for different deduplication strategies

**Implementation Requirements:**
- [ ] Implement robust deduplication algorithms
- [ ] Support exact and fuzzy matching
- [ ] Allow configurable deduplication strategies
- [ ] Maintain audit trail of deduplication decisions

**Acceptance Criteria:**
- Removes exact duplicates with 100% accuracy
- Identifies potential near-duplicates for review
- Provides audit trail of deduplication decisions

**Quality Gate:** Deduplication reduces dataset size while maintaining data integrity

---

## PHASE 7: SNOWFLAKE INTEGRATION SETUP

### 7.1 Snowflake Connection Setup
**Test Requirements:**
- [ ] Write test for Snowflake connection establishment
- [ ] Write test for connection error handling
- [ ] Write test for authentication methods
- [ ] Write test for connection pooling/management

**Implementation Requirements:**
- [ ] Research and set up Snowflake Python connector
- [ ] Implement secure credential management
- [ ] Set up connection pooling for efficiency
- [ ] Implement proper error handling and retries

**Acceptance Criteria:**
- Secure, reliable connection to Snowflake
- Proper credential management (no hardcoded secrets)
- Efficient connection handling

**Quality Gate:** Successful connection to Snowflake data warehouse established

---

### 7.2 Order Data Retrieval
**Test Requirements:**
- [ ] Write test for order data query construction
- [ ] Write test for date range filtering
- [ ] Write test for large result set handling

**Implementation Requirements:**
- [ ] Implement order data retrieval queries
- [ ] Support flexible date range filtering
- [ ] Handle large result sets efficiently

**Acceptance Criteria:**
- Retrieves order data for specified time periods
- Handles large datasets efficiently
- Provides relevant order and product information

**Quality Gate:** Order data successfully retrieved and validated for test periods

---

## PHASE 8: ORDER MATCHING & JOIN

### 8.1 Primary Matching (Tracking Codes)
**Test Requirements:**
- [ ] Write test for exact tracking code matches
- [ ] Write test for tracking code format variations
- [ ] Write test for missing tracking codes
- [ ] Write test for match rate calculation

**Implementation Requirements:**
- [ ] Implement tracking code-based matching
- [ ] Handle tracking code format variations
- [ ] Calculate and report match rates
- [ ] Identify unmatched records for further processing

**Acceptance Criteria:**
- High match rate (target >80%) on tracking codes
- Clear identification of unmatched records
- Robust handling of tracking code variations

**Quality Gate:** Primary matching achieves >80% match rate on test data

---

### 8.2 Secondary Matching (Customer Name + Date)
**Test Requirements:**
- [ ] Write test for customer name fuzzy matching
- [ ] Write test for date range matching
- [ ] Write test for combined customer/date matching
- [ ] Write test for match confidence scoring

**Implementation Requirements:**
- [ ] Implement fuzzy customer name matching
- [ ] Support date range matching (±N days)
- [ ] Combine multiple matching signals
- [ ] Generate confidence scores for matches

**Acceptance Criteria:**
- Improves overall match rate by ≥10 percentage points
- Provides confidence scores for manual review
- Handles name variations and date discrepancies

**Quality Gate:** Combined matching achieves >90% total match rate

---

### 8.3 Match Quality Control
**Test Requirements:**
- [ ] Write test for match validation rules
- [ ] Write test for duplicate match detection
- [ ] Write test for match confidence thresholds
- [ ] Write test for manual review flagging

**Implementation Requirements:**
- [ ] Implement match quality validation
- [ ] Detect and resolve duplicate matches
- [ ] Apply confidence thresholds for auto-acceptance
- [ ] Flag low-confidence matches for review

**Acceptance Criteria:**
- Validates match quality automatically
- Flags ambiguous matches for manual review
- Provides clear match quality metrics

**Quality Gate:** Match quality validation passes with clear quality metrics

---

## PHASE 9: QUALITY CONTROL & OPTIMIZATION

### 9.1 Match Rate Analysis
**Test Requirements:**
- [ ] Write test for match rate calculation by vendor
- [ ] Write test for match rate trends over time
- [ ] Write test for unmatched record analysis
- [ ] Write test for match quality distribution

**Implementation Requirements:**
- [ ] Calculate comprehensive match rate statistics
- [ ] Analyze patterns in unmatched records
- [ ] Generate match rate reports and trends
- [ ] Identify opportunities for improvement

**Acceptance Criteria:**
- Clear visibility into match rates by vendor and time period
- Analysis of unmatched records to identify patterns
- Recommendations for match rate improvement

**Quality Gate:** Match rate analysis complete with actionable insights

---

### 9.2 Data Quality Scoring
**Test Requirements:**
- [ ] Write test for completeness scoring
- [ ] Write test for accuracy validation
- [ ] Write test for consistency checks
- [ ] Write test for overall quality score calculation

**Implementation Requirements:**
- [ ] Implement comprehensive data quality scoring
- [ ] Validate data accuracy and consistency
- [ ] Generate quality scorecards
- [ ] Identify data quality improvement opportunities

**Acceptance Criteria:**
- Comprehensive quality scoring across all dimensions
- Clear identification of data quality issues
- Actionable recommendations for improvement

**Quality Gate:** Data quality scoring shows >95% overall quality score

---

## PHASE 10: WEIGHTED AVERAGE CALCULATION

### 10.1 Cost Aggregation by Product/Size
**Test Requirements:**
- [ ] Write test for shipping cost aggregation
- [ ] Write test for product quantity aggregation  
- [ ] Write test for size-specific calculations
- [ ] Write test for weighted average formula validation

**Implementation Requirements:**
- [ ] Aggregate shipping costs by product type and size
- [ ] Calculate quantity-weighted averages
- [ ] Handle different product categories appropriately
- [ ] Validate calculation accuracy

**Acceptance Criteria:**
- Accurate cost aggregation by product type and size
- Properly weighted averages based on quantities
- Support for different product categories

**Quality Gate:** Cost calculations validated against manual spot checks

---

### 10.2 Final Output Generation
**Test Requirements:**
- [ ] Write test for output table structure
- [ ] Write test for calculation accuracy
- [ ] Write test for output formatting
- [ ] Write test for export functionality

**Implementation Requirements:**
- [ ] Generate final weighted average cost table
- [ ] Include cost per product, per size, per order
- [ ] Support multiple output formats (CSV, Excel, JSON)
- [ ] Include metadata and calculation details

**Acceptance Criteria:**
- Final output table matches required specification
- Calculations are accurate and auditable
- Multiple output formats supported
- Clear documentation of methodology

**Quality Gate:** Final output validated and ready for business use

---

## SUCCESS METRICS

### Overall Quality Gates:
- **Data Coverage:** >95% of invoice records successfully processed
- **Match Rate:** >90% of invoices matched to orders  
- **Data Quality:** >95% overall data quality score
- **Accuracy:** Weighted averages within 5% of manual calculations

### Testing Coverage:
- **Unit Tests:** >90% code coverage
- **Integration Tests:** All major workflows tested end-to-end
- **Data Tests:** All sample files processed successfully
