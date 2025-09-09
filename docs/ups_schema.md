# UPS Invoice Schema Pattern

**Example Analysis**: Single UPS invoice (`UPS_LOL509_08022025.xlsx`) used to understand typical UPS invoice structure and data patterns

## Overview
- **Sample Invoice Records**: 3,284 shipments
- **Sample Date Range**: July-August 2025 (pickup dates in July, invoice dated Aug 2)
- **Typical File Structure**: Excel file with total amount in row 1, column headers in row 2
- **Purpose**: This analysis represents patterns expected across UPS invoices generally

## Fields

### 1. Carrier Invoice Date
- **Coverage**: 100% (3,284/3,284)
- **Type**: Date
- **Values**: Single invoice date: `2025-08-02`
- **Notes**: All shipments on same invoice

### 2. Tracking Number
- **Coverage**: 100%
- **Type**: Text (18 characters)
- **Unique**: All unique (3,284 unique values)
- **Pattern**: `1Z` + alphanumeric (UPS standard format)
- **Sample**: `1ZY4B1990200179471`, `1ZY4B1990200355968`

### 3. Pickup Date
- **Coverage**: 100%
- **Type**: Date
- **Range**: July 18 - August 1, 2025 (18 unique dates)
- **Notes**: Primarily July 2025 pickups

### 4. Reference 1
- **Coverage**: 100%
- **Type**: Text
- **Unique Values**: 965
- **Common Values**: 
  - `LOLAID`: ~2,319 occurrences (70.6%)
  - Order numbers (e.g., `#464294`): remaining 30%
- **Notes**: Mix of account ID and order references

### 5. Reference 2
- **Coverage**: 100%
- **Type**: Text
- **Unique Values**: 3,123 (95% unique)
- **Patterns**:
  - `#` + 6 digits (e.g., `#461433`)
  - `M` + 7 digits (e.g., `M3289744`)
- **Notes**: Dual numbering system for order tracking

### 6. Service
- **Coverage**: 100%
- **Type**: Text (10 service types)
- **Distribution**:
  - Ground Residential: 2,415 (73.5%)
  - Ground: 442 (13.5%)
  - UPS Ground Saver - 1 LB or Greater: 152 (4.6%)
  - Ground Commercial: 108 (3.3%)
  - 2nd Day Air Residential: 99 (3.0%)
  - 2nd Day Air: 54 (1.6%)
  - 2nd Day Air Commercial: 7 (0.2%)
  - Ground Undeliverable Return: 5 (0.2%)
  - Ground Return to Sender: 1 (<0.1%)
  - Invalid entry (0): 1 (<0.1%)

### 7. Billed Weight
- **Coverage**: 100%
- **Type**: Integer (pounds)
- **Range**: 0 - 68 lbs
- **Average**: 12.0 lbs
- **Unique Values**: 39
- **Notes**: Heavier packages than FedEx (avg 12 vs 10 lbs)

### 8. Recipient Name
- **Coverage**: 99.9% (3,282/3,284)
- **Type**: Text
- **Unique Values**: 3,010 (mostly unique)
- **Sample**: Individual and organization names
- **Notes**: High uniqueness indicates individual customers

### 9. Recipient State
- **Coverage**: 100%
- **Type**: 2-letter state code
- **Unique Values**: 52 (all US states + territories)
- **Notes**: Nationwide US distribution

### 10. Recipient Postal Code
- **Coverage**: 100%
- **Type**: Numeric
- **Unique Values**: 2,988 (91% unique)
- **Formats**: Mix of 5-digit and 9-digit ZIP codes
- **Sample**: `37916`, `667705120` (ZIP+4 without hyphen)

### 11. Recipient Country
- **Coverage**: 100%
- **Type**: Text
- **Values**: 
  - `US`: 3,283 (99.97%)
  - Invalid entry (0): 1 (0.03%)
- **Notes**: Almost exclusively domestic US shipments

### 12. Origin State
- **Coverage**: 100%
- **Type**: 2-letter state code
- **Values**:
  - `ID`: 3,282 (99.94%) - Idaho
  - `PA`: 1 (0.03%) - Pennsylvania
  - Invalid entry (0): 1 (0.03%)
- **Notes**: Nearly all shipments originate from Idaho

### 13. Shipping Cost
- **Coverage**: 100%
- **Type**: Decimal (currency)
- **Range**: $0.00 - $129.78
- **Average**: $16.65
- **Unique Values**: 415
- **Notes**: Lower average cost than FedEx ($16.65 vs $28.67)

## Key Observations (Based on Sample Invoice)

1. **Service Mix**: Heavily ground-focused (90.1% ground services vs 9.9% expedited)
2. **Weight Profile**: Slightly heavier packages than FedEx (12 lbs vs 10 lbs average)
3. **Cost Structure**: Significantly lower average shipping cost ($16.65 vs $28.67 FedEx)
4. **Geographic Origin**: Concentrated shipping from Idaho (99.94%)
5. **Reference System**: Dual tracking with LOLAID constant and order numbers
6. **Volume**: Much higher shipment volume (3,284 vs 888 FedEx)

## Expected Invoice Pattern

This schema represents the typical structure and data patterns expected across UPS invoices:
- Consistent 13-field structure with essential shipping data
- Reference fields for order tracking integration
- Service-focused data without package dimensions
- Direct shipping cost reporting
- Geographic origin tracking

## Comparison with FedEx (Sample Invoices)

| Metric | UPS | FedEx |
|--------|-----|-------|
| **Sample Shipments** | 3,284 | 888 |
| **Primary Services** | Ground (90%) | SmartPost/2Day (82%) |
| **Avg Weight** | 12.0 lbs | 10.3 lbs (billed) |
| **Avg Cost** | $16.65 | $28.67 |
| **Origin Patterns** | ID (99.9%) | Multiple |
| **Service Focus** | Economy ground | Mixed economy/expedited |

## Data Quality Issues

- **Invalid entries**: Some records contain `0` values in text fields
- **ZIP code formatting**: Mix of 5 and 9-digit codes without standardization
- **Missing recipients**: 2 records lack recipient names
- **Service type anomaly**: One invalid service type entry (0)

## Schema Differences from FedEx

1. **Simpler structure**: 13 fields vs 20 (FedEx)
2. **No dimensional data**: UPS file lacks package dimensions
3. **Different reference system**: LOLAID + order numbers vs M-numbers + #-numbers
4. **Service naming**: UPS uses descriptive names, FedEx uses brand names
5. **Date fields**: UPS has pickup date, FedEx has ship date
6. **Cost transparency**: UPS shows shipping cost directly, FedEx shows net charge
7. **No zone information**: UPS file doesn't include shipping zones