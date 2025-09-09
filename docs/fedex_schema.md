# FedEx Invoice Schema Pattern

**Example Analysis**: Single FedEx invoice (`FDX_20250802_LOL509.xlsx`) used to understand typical FedEx invoice structure and data patterns

## Overview
- **Sample Invoice Records**: 888 shipments
- **Sample Date Range**: July 2025 (various ship dates, single invoice date)
- **Typical File Structure**: Excel file with header rows (invoice total in row 1, column headers in row 3)
- **Purpose**: This analysis represents patterns expected across FedEx invoices generally

## Fields

### 1. Tracking Number
- **Coverage**: 100% (888/888)
- **Type**: Numeric (12 digits)
- **Unique**: All unique (888 unique values)
- **Sample**: `391384417170`, `391194365943`

### 2. Invoice Date
- **Coverage**: 100%
- **Type**: Date
- **Values**: Single invoice date: `7/31/2025`
- **Notes**: All shipments on same invoice

### 3. Ship Date
- **Coverage**: 100%
- **Type**: Date
- **Range**: July 1-28, 2025 (17 unique dates)
- **Distribution**: Scattered throughout July 2025

### 4. Service Type
- **Coverage**: 100%
- **Type**: Text (6 service levels)
- **Distribution**:
  - SmartPost: 474 (53.4%)
  - FedEx 2Day: 258 (29.1%)
  - Home Delivery: 107 (12.0%)
  - Ground: 39 (4.4%)
  - FedEx Priority Overnight: 6 (0.7%)
  - FedEx Standard Overnight: 4 (0.4%)

### 5. Actual Weight
- **Coverage**: 100%
- **Type**: Decimal (pounds)
- **Range**: 1.0 - 34.0 lbs
- **Average**: 8.1 lbs
- **Unique Values**: 144

### 6. Billed Weight
- **Coverage**: 100%
- **Type**: Integer (pounds)
- **Range**: 1 - 50 lbs
- **Average**: 10.3 lbs
- **Notes**: Often higher than actual weight (dimensional weight pricing)

### 7-9. Package Dimensions
- **Coverage**: 100% each
- **Type**: Decimal (inches)
- **Dim Length**: 0-28 inches (17 unique values)
- **Dim Width**: 0-29 inches (17 unique values)
- **Dim Height**: 0-20 inches (16 unique values)
- **Notes**: Some zero values present

### 10. Recipient Company
- **Coverage**: 99.8% (886/888)
- **Type**: Text
- **Unique Values**: 851 (mostly unique)
- **Notes**: Individual customer names

### 11. Recipient Contact
- **Coverage**: 58.2% (517/888)
- **Type**: Text
- **Unique Values**: 502
- **Notes**: Optional field, often missing

### 12. Recipient State
- **Coverage**: 100%
- **Type**: 2-letter state code
- **Unique Values**: 52 (all US states + territories)
- **Notes**: Nationwide distribution

### 13. Recipient Zipcode
- **Coverage**: 100%
- **Type**: Numeric (5 or 9 digit)
- **Unique Values**: 765
- **Notes**: Mix of 5-digit and ZIP+4 formats

### 14. Recipient Country
- **Coverage**: 100%
- **Type**: Text
- **Values**: "US" only
- **Notes**: All domestic shipments

### 15. Reference 1
- **Coverage**: 99.2% (881/888)
- **Type**: Text (order numbers)
- **Pattern**: `M` + 6 digits (e.g., `M931508`)
- **Unique Values**: 864 (mostly unique)

### 16. Reference 2
- **Coverage**: 100%
- **Type**: Text (order references)
- **Pattern**: `#` + 5-6 digits (e.g., `#459871`)
- **Unique Values**: 869 (mostly unique)

### 17. Reference 3
- **Coverage**: 0% (unused field)
- **Type**: Empty
- **Notes**: Column exists but no data

### 18. Reference 4
- **Coverage**: 100%
- **Type**: Text
- **Values**: "LOL509" (constant)
- **Notes**: Company/account identifier

### 19. Zone
- **Coverage**: 100%
- **Type**: Mixed format (2-digit with leading zero, single digit, letters)
- **Values**: 18 unique zones (02-12, 2-8, A, M)
- **Notes**: Inconsistent formatting (both "05" and "5" formats)
- **Distribution**: Zone 4/04 most common (217 shipments)

### 20. Net Charge
- **Coverage**: 100%
- **Type**: Currency (formatted with $)
- **Range**: $8.37 - $192.47
- **Average**: $28.67
- **Notes**: Final shipping cost after all fees/discounts

## Key Observations (Based on Sample Invoice)

1. **Service Mix**: Primarily economy services (SmartPost 53%, 2Day 29%)
2. **Weight Profile**: Small packages averaging 8 lbs actual, 10 lbs billed
3. **Geographic Spread**: Nationwide US distribution across all zones
4. **Reference System**: Dual reference system (M-numbers and #-numbers) for order tracking
5. **Data Quality**: High completeness except for optional Recipient Contact field
6. **Zone Formatting**: Inconsistent zone code formatting needs standardization
7. **Package Dimensions**: Consistent but some zero values suggest missing measurements

## Expected Invoice Pattern

This schema represents the typical structure and data patterns expected across FedEx invoices:
- Consistent 20-field structure with standard shipping data
- Reference fields for order tracking integration
- Comprehensive package dimension and weight data
- Zone-based pricing information
- Mixed service levels from economy to overnight

## Data Quality Issues

- **Zone formatting inconsistency**: Mix of "05" and "5" formats
- **Missing recipient contacts**: 42% of records lack contact names
- **Unused Reference 3 field**: Column exists but empty
- **Zero dimensions**: Some packages show 0 for length/width/height