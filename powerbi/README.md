# Power BI Build Guide

Save your final Power BI Desktop file in this folder after connecting to MySQL.

## Recommended data source

- Connector: `MySQL database`
- Server: `localhost`
- Database: `retail_sales_analytics`
- Main table/view: `retail_sales_view`
- Data mode: `Import`

## Final report pages

1. Executive Overview
   - KPI cards: Total Revenue, Total Profit, Profit Margin %, Average Order Value, Units Sold, Total Orders, Total Customers
   - Line chart: Monthly Revenue and Profit
   - Combo chart: Discount Impact on Revenue and Profit
   - Column chart: Revenue by Sales Channel
   - Slicers: Year, Region, Category, Sales Channel

2. Product Performance
   - Clustered bar chart: Category Revenue and Profit
   - Table: Top Products by Revenue and Profit
   - Table: Products to Promote
   - Table: Products to Review
   - Slicers: Year, Region, Category, Sales Channel

3. Customer and Region
   - Clustered bar chart: Regional Revenue and Profit
   - Matrix: Revenue by Region and Customer Segment
   - Donut chart: Revenue by Customer Segment
   - Table: Top Customers by Revenue
   - Slicers: Year, Region, Sales Channel

## Suggested DAX measures

```dax
Total Revenue = SUM(retail_sales_view[net_sales])
Total Profit = SUM(retail_sales_view[profit])
Units Sold = SUM(retail_sales_view[quantity])
Total Orders = DISTINCTCOUNT(retail_sales_view[order_id])
Total Customers = DISTINCTCOUNT(retail_sales_view[customer_id])
Average Order Value = DIVIDE([Total Revenue], [Total Orders])
Profit Margin % = DIVIDE([Total Profit], [Total Revenue])
```

## Supporting files

- `measures.dax` contains the reusable DAX measures.
- `dashboard_blueprint.md` contains the full page-by-page build plan.
- Save your final `.pbix` file in this folder for the portfolio repo.
