# Tableau Build Guide

Save your Tableau workbook in this folder as `retail_sales_dashboard.twbx` after you connect to MySQL.

## Recommended sheets

1. Monthly Sales Trend
   - Columns: `order_date` by month
   - Rows: `SUM(net_sales)` and `SUM(profit)`

2. Category Performance
   - Bars: `category`
   - Color or label: `SUM(profit)`

3. Top Customers
   - Bars: `customer_name`
   - Measure: `SUM(net_sales)`
   - Filter to Top 10 by revenue

4. Regional Performance
   - Bars or filled map: `region`
   - Measure: `SUM(net_sales)`

5. Discount Impact
   - Calculated discount band:

```tableau
IF [discount] = 0 THEN "No Discount"
ELSEIF [discount] <= 0.10 THEN "1-10%"
ELSEIF [discount] <= 0.20 THEN "11-20%"
ELSE "Above 20%"
END
```

## Dashboard idea

Combine the sheets into one public-facing dashboard with a date filter, region filter, and category filter. Use the MySQL view `retail_sales_view` as the primary source to keep the workbook simple.

