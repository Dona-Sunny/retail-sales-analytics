# Power BI Build Guide

Save your Power BI Desktop file in this folder as `retail_sales_dashboard.pbix` after you connect to MySQL.

## Recommended pages

1. Executive Overview
   - KPI cards: Total Revenue, Total Profit, Profit Margin %, Average Order Value, Units Sold
   - Line chart: Monthly Revenue and Profit
   - Slicers: Year, Region, Category, Sales Channel

2. Product Performance
   - Clustered bar chart: Revenue by Category
   - Table: Top 10 Products by Revenue and Profit
   - Scatter plot: Revenue vs Profit by Product

3. Customer and Region
   - Bar chart: Revenue by Region
   - Table: Top Customers
   - Donut chart: Revenue by Customer Segment

## Suggested DAX measures

```dax
Total Revenue = SUM(retail_sales_view[net_sales])
Total Profit = SUM(retail_sales_view[profit])
Units Sold = SUM(retail_sales_view[quantity])
Average Order Value = DIVIDE([Total Revenue], DISTINCTCOUNT(retail_sales_view[order_id]))
Profit Margin % = DIVIDE([Total Profit], [Total Revenue])
```

## Data source

Use the MySQL view `retail_sales_view` as the main model table. It already includes the calculated revenue, discount, cost, and profit columns needed for dashboarding.

