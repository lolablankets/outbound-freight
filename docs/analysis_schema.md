# Analysis Schema Documentation

This document defines the three key schemas used in the outbound freight analysis pipeline, derived from actual example data and vendor invoice patterns.

## 1. Common Invoice Schema (Unified)

This is the normalized schema all vendor invoice data is mapped to before analysis.

### Fields

| Field Name | Type | Required | Source Mappings | Notes |
|------------|------|----------|----------------|-------|
| `tracking_number` | String | Yes | FedEx: "Tracking Number", UPS: "Tracking Number" | Primary key for shipments |
| `vendor` | Enum | Yes | Derived from filename | FEDEX, UPS, USPS, UNKNOWN |
| `invoice_date` | Date | Yes | FedEx: "Invoice Date", UPS: "Carrier Invoice Date" | |
| `ship_date` | Date | Yes | FedEx: "Ship Date", UPS: "Pickup Date" | Date package was picked up |
| `service_type` | String | Yes | FedEx: "Service Type", UPS: "Service" | Normalized service names |
| `shipping_cost` | Decimal | Yes | FedEx: "Net Charge", UPS: "Shipping Cost" | Final cost after discounts |
| `actual_weight` | Decimal | No | FedEx: "Actual Weight", UPS: N/A | Physical weight in lbs |
| `billed_weight` | Integer | Yes | FedEx: "Billed Weight", UPS: "Billed Weight" | Charged weight in lbs |
| `recipient_name` | String | Yes | FedEx: "Recipient Company", UPS: "Recipient Name" | Customer name |
| `recipient_state` | String | Yes | FedEx: "Recipient State", UPS: "Recipient State" | 2-letter state code |
| `recipient_zip` | String | Yes | FedEx: "Recipient Zipcode", UPS: "Recipient Postal Code" | ZIP code (normalized) |
| `recipient_country` | String | Yes | FedEx: "Recipient Country", UPS: "Recipient Country" | Country code |
| `origin_state` | String | No | UPS: "Origin State", FedEx: N/A | Ship-from location |
| `reference_1` | String | No | FedEx: "Reference 1" (M-numbers), UPS: "Reference 1" (LOLAID) | Primary order reference |
| `reference_2` | String | No | FedEx: "Reference 2" (#-numbers), UPS: "Reference 2" (#-numbers) | Secondary order reference |
| `reference_4` | String | No | FedEx: "Reference 4" (LOL509), UPS: N/A | Account identifier |
| `zone` | String | No | FedEx: "Zone", UPS: N/A | Shipping zone |
| `package_length` | Decimal | No | FedEx: "Dim Length", UPS: N/A | Package dimensions (inches) |
| `package_width` | Decimal | No | FedEx: "Dim Width", UPS: N/A | Package dimensions (inches) |
| `package_height` | Decimal | No | FedEx: "Dim Height", UPS: N/A | Package dimensions (inches) |

### Data Quality Standards
- **Required fields**: Must be present and non-null
- **Tracking numbers**: Must be unique within the dataset
- **Dates**: Converted to standard datetime format
- **Currency**: Decimal format, no currency symbols
- **ZIP codes**: Normalized to consistent format
- **State codes**: Validated 2-letter US state codes

---

## 2. Intermediate Order Schema (With Product Quantities)

This schema represents orders after joining invoice data with Shopify order data, showing product quantities per order.

### Fields

| Field Name | Type | Description | Example Values |
|------------|------|-------------|----------------|
| `order_id` | String | Shopify order reference | "#355467", "#464294" |
| `month` | Integer | Order month for aggregation | 4, 7, 8 |
| `large` | Integer | Large blanket quantity | 0, 1, 2, 4, 16, 60 |
| `medium` | Integer | Medium blanket quantity | 0, 1, 2, 30 |
| `baby` | Integer | Baby blanket quantity | 0, 1, 2, 8 |
| `xl_or_wtd` | Integer | XL/Weighted blanket quantity | 0, 1, 2 |
| `lg_pet_bed` | Integer | Large pet bed quantity | 0, 1 |
| `pillow_square` | Integer | Square pillow quantity | 0 (tracked but unused) |
| `pillow_lumbar` | Integer | Lumbar pillow quantity | 0 (tracked but unused) |
| `gift_bag` | Integer | Gift bag quantity | 0, 1, 2 |
| `other` | Integer | Other product quantity | 0, 1, 2 |
| `blankets` | Integer | Total blanket count | sum(large + medium + baby + xl_or_wtd) |
| `total_shipping` | Currency | Total shipping cost for order | $11.30 - $1,133.83 |
| `order_date` | Datetime | When order was placed | 4/1/2025 8:04:52 AM |

### Data Quality Metrics (from example data)
- **Total Orders**: 38,805
- **Orders Missing**: 139 (0.36% miss rate)
- **Order ID Pattern**: Primarily "#" + 6 digits
- **Date Range**: April 2025 in example data
- **Shipping Cost Range**: $11.30 to $1,133.83

---

## 3. Final Output Schema (Weighted Average Analysis)

This is the final aggregated schema showing weighted average costs per product type across different order combinations.

### Fields

| Field Name | Type | Description | Calculation Method |
|------------|------|-------------|-------------------|
| `large` | Integer | Large blankets in order combination | Direct count |
| `medium` | Integer | Medium blankets in order combination | Direct count |
| `baby` | Integer | Baby blankets in order combination | Direct count |
| `xl_or_wtd` | Integer | XL/Weighted blankets in order combination | Direct count |
| `lg_pet_bed` | Integer | Large pet beds in order combination | Direct count |
| `pillow_square` | Integer | Square pillows in order combination | Direct count |
| `pillow_lumbar` | Integer | Lumbar pillows in order combination | Direct count |
| `gift_bag` | Integer | Gift bags in order combination | Direct count |
| `other` | Integer | Other products in order combination | Direct count |
| `avg_order_shipping_cost` | Currency | Average shipping cost for this combination | Mean of total_shipping for matching orders |
| `count_of_orders` | Integer | Number of orders with this exact combination | COUNT(*) |
| `orders_share` | Percentage | Share of total orders | count_of_orders / total_orders |
| `cost_per_product` | Currency | Shipping cost per individual item | avg_order_shipping_cost / total_items |
| `large_blanket_units` | Integer | Total large blanket units across all orders | SUM(large * count_of_orders) |
| `large_share` | Percentage | Share of total large blankets | large_blanket_units / total_large_units |
| `medium_blanket_units` | Integer | Total medium blanket units | SUM(medium * count_of_orders) |
| `medium_share` | Percentage | Share of total medium blankets | medium_blanket_units / total_medium_units |
| `baby_blanket_units` | Integer | Total baby blanket units | SUM(baby * count_of_orders) |
| `baby_share` | Percentage | Share of total baby blankets | baby_blanket_units / total_baby_units |
| `xl_wtd_blanket_units` | Integer | Total XL/weighted blanket units | SUM(xl_or_wtd * count_of_orders) |
| `xl_wtd_share` | Percentage | Share of total XL/weighted blankets | xl_wtd_blanket_units / total_xl_wtd_units |
| `pillow_units` | Integer | Total pillow units (square + lumbar) | SUM((pillow_square + pillow_lumbar) * count_of_orders) |
| `pillow_share` | Percentage | Share of total pillows | pillow_units / total_pillow_units |
| `lg_pet_bed_units` | Integer | Total large pet bed units | SUM(lg_pet_bed * count_of_orders) |
| `lg_pet_bed_share` | Percentage | Share of total pet beds | lg_pet_bed_units / total_pet_bed_units |
| `all_blankets` | Integer | Total blanket units in this combination | large + medium + baby + xl_or_wtd |
| `blanket_share` | Percentage | Share of total blankets | all_blankets / total_blanket_units |

### Summary Calculations (Right Side Columns)
- **Overall Weighted Avg Cost per Product**: Calculated per product type
  - Large: $16.00
  - Medium: $13.40  
  - Baby: $11.23
  - XL/Wtd: $16.22
  - Lg Pet Bed: $20.27
  - Pillows: $9.23
  - Order Average: $19.85
  - Blanket Average: $14.93

### Special Cases
- **"Other" products**: No cost per product calculated (shows blank in cost_per_product)
- **Gift bags**: Treated as accessories, contribute to total cost division
- **Empty combinations**: Orders with only "Other" or only gift accessories

---

## Data Flow Summary

1. **Vendor Invoices** ’ **Common Schema**: Normalize fields from FedEx/UPS/USPS invoices
2. **Common Schema** + **Shopify Orders** ’ **Intermediate Schema**: Join on tracking numbers/order references
3. **Intermediate Schema** ’ **Final Schema**: Aggregate by product combinations and calculate weighted averages

## Business Logic Notes

1. **Weighted Averages**: Based on quantity of each product type across all orders
2. **Product Categories**: Blankets are the primary focus, with accessories (pillows, pet beds) calculated separately
3. **Order Combinations**: Each unique combination of products gets its own weighted average
4. **Cost Allocation**: Total shipping cost divided by number of items in order to get per-product cost
5. **Share Calculations**: Both order share (% of total orders) and unit share (% of total units) are tracked

This schema supports the business goal of determining fair shipping cost allocation per product type for pricing and profitability analysis.