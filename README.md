On a monthly basis we are provided with invoices for FedEx, UPS, and USPS. We need to clean and extract relevant data from these invoices, combine the data into a unified schema, join it to Shopify order data to retrieve information per order on product quantities per size, and use this data to derive a weighted average cost per item for each type of product we sell. 

The end output will be a table with a weighted avg. cost per product for each size, per order, and per blanket on average. 

Steps we need to take: 
1. Read XLSX/CSV files and note properly which vendor they come from based on file name (FDX or UPS or USPS)
2. Read in the spreadsheet - note that the headers are not always in row 1. We need to consistently detect the proper headers in the file and it's sometimes dynamic what row they start in 
3. Clean fields - it's a bit of a TBD what we will need to catch but there will be commmon cases that we can build shared utilities for. For example, converting dollar sign text to decimal: $38.33 -> 38.33, date string to date 7/31/2025 12:00:00 AM -> actual date, normalizing field names to lowercase with _ in between. 
4. Map the key fields we need to the possible field names in different invoices - we will need a common set of data points from each invoice and can robustly handle name/schema drift over time if we say "these 3 names from FedEx invoices can all correspond to this data point we need" 
5. Retrieve the data we need from each invoice into our shared schema 
6. Consolidate all data into one place and de-dupe just in case
7. Retrieve order data from our Snowflake data warehouse for the same timeframe
8. Join order data onto invoices using order codes to pull in # of large, small, weighted blanket, etc. units as it matters 
9. QC - how many invoice orders, how many matched, etc? And we may need to invent some more matching mechanisms to increase match rate like matching on custoimer name and oirder date. TBD. 
10. Prepare final aggregation table where we get total cost per order of shipping, share of quantity by size/type, and use that to calculate a weighted average of the shipping cost per unit/type 