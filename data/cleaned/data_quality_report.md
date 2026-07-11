# Data Quality Report

The synthetic raw dataset was intentionally seeded with a few realistic data-quality issues and then cleaned into the final analysis-ready file.

## Issues corrected

- Removed `20` rows with missing keys or invalid order dates.
- Removed `24` duplicate transaction rows based on `Order_ID + Product_ID`.
- Standardized category names such as `electronics`, `Electronic`, and `ELECTRONICS` to `Electronics`.
- Trimmed extra spaces and normalized capitalization in customer segments, cities, channels, and product categories.
- Converted percentage-style discounts such as `15` into decimal form `0.15`.
- Converted dates to the standard `YYYY-MM-DD` format.
- Recalculated `Gross_Sales`, `Discount_Amount`, `Net_Sales`, `Total_Cost`, and `Profit`.

## Final result

- Raw transaction rows: `5,535`
- Cleaned transaction rows: `5,491`
- Customers: `615`
- Products: `120`
- Orders: `2,598`
- Date range: `2024-01-01` to `2025-12-31`

