# TODO: Outbound Freight Invoice Processing Pipeline

## Overview
Process shipping invoices from FedEx, UPS, and USPS to calculate weighted average shipping costs per product. Follow **TEST-DRIVEN DEVELOPMENT (TDD)** - write tests first, then implementation.

---

## PHASE 1: VENDOR DETECTION & FILE READING

### 1.1 Vendor Detection from Filenames ✅
**Test Requirements:**
- [x] Write test for FedEx detection: files containing 'fdx', 'fedex' (case insensitive) - Comprehensive test suite with 19 test cases
- [x] Write test for UPS detection: files containing 'ups' (case insensitive) - Multiple case variations tested
- [x] Write test for USPS detection: files containing 'usps', 'stamps' (case insensitive) - Full keyword coverage
- [x] Write test for unknown vendor fallback - Edge cases for unrecognized patterns
- [x] Write test against actual sample files in `data/2025/08/` - All 10 sample files validated

**Implementation Requirements:**
- [x] Implement robust vendor detection function - Position-based priority matching algorithm
- [x] Handle edge cases (multiple vendor keywords, special characters) - First-match-wins logic implemented
- [x] Return appropriate Vendor enum values - FEDEX, UPS, USPS, UNKNOWN enum structure

**Acceptance Criteria:**
- 100% of test sample files correctly identified ✅
- Function handles malformed filenames gracefully ✅

**Quality Gate:** All vendor detection tests pass with 100% accuracy on sample data ✅ (19/19 tests passing, 10/10 sample files correct)

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
- [ ] Write test for FedEx-specific field variations:
  - [ ] "Tracking Number" (12-digit numeric) → tracking_number
  - [ ] "Invoice Date" → invoice_date 
  - [ ] "Ship Date" → ship_date
  - [ ] "Service Type" → service_type (SmartPost, FedEx 2Day, etc.)
  - [ ] "Net Charge" (with $) → shipping_cost
  - [ ] "Actual Weight"/"Billed Weight" → actual_weight/billed_weight
  - [ ] "Recipient Company" → recipient_name
  - [ ] "Reference 1" (M-numbers like "M931508") → reference_1
  - [ ] "Reference 2" (#-numbers like "#459871") → reference_2
  - [ ] "Reference 4" ("LOL509" account ID) → reference_4
  - [ ] "Zone" (inconsistent format: "05" vs "5") → zone
  - [ ] Package dimensions: "Dim Length/Width/Height" → package_*
- [ ] Write test against actual FedEx sample files
- [ ] Write test for missing field handling
- [ ] Write test for zone format normalization ("05" → "5")

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
- [ ] Write test for UPS-specific field variations:
  - [ ] "Tracking Number" (18-char: "1Z" + alphanumeric) → tracking_number
  - [ ] "Carrier Invoice Date" → invoice_date
  - [ ] "Pickup Date" → ship_date
  - [ ] "Service" → service_type (Ground Residential, 2nd Day Air, etc.)
  - [ ] "Shipping Cost" (direct cost field) → shipping_cost
  - [ ] "Billed Weight" (no actual weight field) → billed_weight
  - [ ] "Recipient Name" → recipient_name
  - [ ] "Reference 1" ("LOLAID" ~70% + order numbers ~30%) → reference_1
  - [ ] "Reference 2" (#-numbers + M-numbers) → reference_2
  - [ ] "Origin State" (99.9% "ID") → origin_state
- [ ] Write test against actual UPS sample files  
- [ ] Write test for missing field handling
- [ ] Write test for handling invalid entries (value "0" in text fields)

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

## PHASE 4.5: PRODUCT CATEGORIES & BUSINESS RULES

### 4.5.1 Product Category Definitions
**Test Requirements:**
- [ ] Write test for product category classification
- [ ] Write test for category validation rules
- [ ] Write test against historical order data patterns

**Implementation Requirements:**
- [ ] Define product categories based on business requirements:
  - [ ] **Large Blankets**: Primary product, individual shipping cost calculation
  - [ ] **Medium Blankets**: Primary product, individual shipping cost calculation  
  - [ ] **Baby Blankets**: Primary product, individual shipping cost calculation
  - [ ] **XL/Weighted Blankets**: Primary product, individual shipping cost calculation
  - [ ] **Large Pet Beds**: Standalone product, individual shipping cost calculation
  - [ ] **Pillows**: Square + Lumbar combined, individual shipping cost calculation
  - [ ] **Gift Bags**: Accessories, contribute to total shipping cost division
  - [ ] **Other**: Special case - no individual cost calculation (blank cost_per_product)

**Acceptance Criteria:**
- Clear category definitions for all product types
- Business rules for cost allocation per category
- Special handling for "Other" category (no per-product cost)

**Quality Gate:** Product categorization matches historical data patterns

---

### 4.5.2 Order Combination Business Logic
**Test Requirements:**
- [ ] Write test for order combination aggregation
- [ ] Write test for weighted average calculations
- [ ] Write test for share percentage calculations
- [ ] Write test for edge cases (single product orders, bulk orders)

**Implementation Requirements:**
- [ ] Aggregate orders by unique product combinations
- [ ] Calculate weighted averages based on quantities:
  - [ ] Total shipping cost ÷ total items = cost per product
  - [ ] Weight by quantity of each product type across all orders
  - [ ] Track both order share (% of orders) and unit share (% of units)
- [ ] Handle special combinations:
  - [ ] Orders with only "Other" products (no cost per product)
  - [ ] Mixed orders with blankets + accessories
  - [ ] Bulk orders (e.g., 30, 60 unit orders in example data)

**Acceptance Criteria:**
- Accurate weighted average calculations per product type
- Proper handling of all order combination types
- Share calculations sum to 100% across categories

**Quality Gate:** Weighted averages match manual calculations within 5%

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
- [ ] Write test for tracking code format variations:
  - [ ] FedEx: 12-digit numeric (e.g., "391384417170")
  - [ ] UPS: 18-character "1Z" + alphanumeric (e.g., "1ZY4B1990200179471")
  - [ ] USPS: Various formats (to be determined from sample data)
- [ ] Write test for missing tracking codes
- [ ] Write test for match rate calculation
- [ ] Write test for duplicate tracking code handling

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
- [ ] Write test for order reference matching:
  - [ ] FedEx Reference 1: M-numbers (e.g., "M931508") → Order ID matching
  - [ ] FedEx Reference 2: #-numbers (e.g., "#459871") → Direct order ID
  - [ ] UPS Reference 1: "LOLAID" (70%) + order numbers (30%)
  - [ ] UPS Reference 2: #-numbers + M-numbers (dual system)
- [ ] Write test for account identifier validation (FedEx Reference 4: "LOL509")

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

## PHASE 8.5: SPECIAL CASE HANDLING

### 8.5.1 Shipping Service Edge Cases
**Test Requirements:**
- [ ] Write test for UPS service variations:
  - [ ] "Ground Undeliverable Return" (5 records in sample)
  - [ ] "Ground Return to Sender" (1 record in sample) 
  - [ ] Invalid service entries (value "0")
- [ ] Write test for FedEx service edge cases:
  - [ ] Overnight services (Priority/Standard)
  - [ ] International shipments (if any)
- [ ] Write test for cost handling of returns and undeliverable packages

**Implementation Requirements:**
- [ ] Handle return shipments appropriately in cost calculations
- [ ] Flag undeliverable/return packages for separate analysis
- [ ] Decide whether to include/exclude returns in weighted averages
- [ ] Handle invalid service type entries gracefully

**Acceptance Criteria:**
- Clear business rules for handling returns and undeliverable packages
- Appropriate cost allocation for edge case services
- Proper flagging and reporting of unusual service types

**Quality Gate:** All edge case services handled according to business rules

---

### 8.5.2 Data Quality Edge Cases
**Test Requirements:**
- [ ] Write test for missing recipient information (2/3,284 UPS records)
- [ ] Write test for invalid country codes (value "0")
- [ ] Write test for missing Reference 3 field (FedEx - unused column)
- [ ] Write test for ZIP code format variations (5-digit vs ZIP+4)
- [ ] Write test for extreme shipping costs ($1,133.83 in example)

**Implementation Requirements:**
- [ ] Handle missing recipient names (use alternative identifiers)
- [ ] Standardize ZIP code formats (5-digit vs 9-digit)
- [ ] Validate and clean invalid entries (value "0" in text fields)
- [ ] Flag extreme outlier costs for manual review
- [ ] Handle unused fields appropriately

**Acceptance Criteria:**
- Robust handling of all data quality issues found in sample data
- Consistent data cleaning across all vendor formats
- Outlier detection and flagging system

**Quality Gate:** Data quality issues handled with <1% data loss

---

### 8.5.3 Historical Data Validation
**Test Requirements:**
- [ ] Write test validating against known match rate (0.36% missing orders)
- [ ] Write test for order volume validation (38,805 orders in example)
- [ ] Write test for cost distribution validation
- [ ] Write test for product mix validation

**Implementation Requirements:**
- [ ] Compare processed results against historical benchmarks
- [ ] Validate order counts and match rates
- [ ] Check product distribution patterns
- [ ] Flag significant deviations from expected patterns

**Acceptance Criteria:**
- Match rates within expected ranges (target: <1% missing orders)  
- Product distributions align with historical patterns
- Cost distributions fall within expected ranges

**Quality Gate:** Results validate against historical data patterns

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
- [ ] Write test for calculation accuracy against known values:
  - [ ] Large Blankets: $16.00 weighted average
  - [ ] Medium Blankets: $13.40 weighted average
  - [ ] Baby Blankets: $11.23 weighted average
  - [ ] XL/Weighted Blankets: $16.22 weighted average
  - [ ] Large Pet Beds: $20.27 weighted average
  - [ ] Pillows: $9.23 weighted average
  - [ ] Overall Order Average: $19.85
  - [ ] Overall Blanket Average: $14.93
- [ ] Write test for share percentage calculations (must sum to 100%)
- [ ] Write test for handling "Other" category (no cost per product)
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
