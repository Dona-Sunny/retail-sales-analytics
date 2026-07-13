# Power BI Dashboard Blueprint

Use this blueprint to build a report that answers every project goal from the `retail_sales_view` table in Power BI Desktop.

## Recommended data source

- Power BI Desktop
- `Get Data` -> `MySQL database`
- Server: `localhost`
- Database: `retail_sales_analytics`
- Main table/view: `retail_sales_view`
- Recommended mode: `Import`

Using the view keeps the report simple because revenue, cost, profit, discount, category, region, customer, and date fields are already joined together.

## Dashboard goal map

| Project question | Best report page | Main visuals |
|---|---|---|
| How much revenue and profit is the business generating? | Executive Overview | KPI cards, trend chart |
| Which products and categories perform best? | Product Performance | Category bar chart, top products table |
| Which regions have the highest sales? | Customer and Region | Region bar chart or map |
| Who are the most valuable customers? | Customer and Region | Top customers table |
| How are sales changing month over month? | Executive Overview | Monthly line chart |
| Are discounts reducing profitability? | Executive Overview or Product Performance | Discount band chart |
| Which products should the business promote or review? | Product Performance | Promote/review tables |

## Model setup

After loading `retail_sales_view`, do the following:

1. Set `order_date` to type `Date`.
2. Format money fields as currency:
   - `net_sales`
   - `profit`
   - `gross_sales`
   - `discount_amount`
   - `total_cost`
3. Sort month labels properly:
   - use `order_month` sorted by `order_month_number`
4. Create the measures from [measures.dax](C:\Users\donas\OneDrive\Desktop\MySQL\powerbi\measures.dax).

## Page 1: Executive Overview

This page should answer:
- How much revenue and profit is the business generating?
- How are sales changing month over month?
- Are discounts reducing profitability?

### Recommended visuals

1. KPI cards
   - Total Revenue
   - Total Profit
   - Profit Margin %
   - Average Order Value
   - Units Sold
   - Total Orders
   - Total Customers

2. Monthly trend line chart
   - Axis: `order_date` by month
   - Values: `Total Revenue`, `Total Profit`

3. Discount analysis combo chart
   - Axis: `Discount Group`
   - Column values: `Total Revenue`
   - Line values: `Profit Margin %`

4. Sales channel chart
   - Axis: `sales_channel`
   - Values: `Total Revenue`

5. Slicers
   - Year
   - Region
   - Category
   - Sales Channel

### Suggested layout

- Top row: KPI cards
- Middle left: monthly sales trend
- Middle right: revenue by sales channel
- Bottom full-width: discount analysis

## Page 2: Product Performance

This page should answer:
- Which products and categories perform best?
- Which products should the business promote or review?

### Recommended visuals

1. Category performance bar chart
   - Axis: `category`
   - Values: `Total Revenue`, `Total Profit`

2. Top products table
   - Columns:
     - `product_name`
     - `category`
     - `Units Sold`
     - `Total Revenue`
     - `Total Profit`
     - `Profit Margin %`
   - Sort by `Total Revenue` descending

3. Promote products table
   - Filter: high profit or top revenue
   - Columns:
     - `product_name`
     - `category`
     - `Total Revenue`
     - `Total Profit`
     - `Profit Margin %`

4. Review products table
   - Filter: negative profit or low margin
   - Columns:
     - `product_name`
     - `category`
     - `Total Revenue`
     - `Total Profit`
     - `Profit Margin %`

5. Optional scatter chart
   - X-axis: `Total Revenue`
   - Y-axis: `Total Profit`
   - Details: `product_name`
   - Legend: `category`

### Suggested layout

- Left: category chart
- Right: scatter chart or top products table
- Bottom: promote products and review products tables

## Page 3: Customer and Region

This page should answer:
- Which regions have the highest sales?
- Who are the most valuable customers?

### Recommended visuals

1. Region bar chart
   - Axis: `region`
   - Values: `Total Revenue`, `Total Profit`

2. Customer segment donut or bar chart
   - Axis/Legend: `customer_segment`
   - Values: `Total Revenue`

3. Top customers table
   - Columns:
     - `customer_name`
     - `customer_segment`
     - `Total Orders`
     - `Total Revenue`
     - `Total Profit`
   - Sort by `Total Revenue` descending

4. Region x customer matrix
   - Rows: `region`
   - Columns: `customer_segment`
   - Values: `Total Revenue`

5. Optional map
   - Location: `city` or `province`
   - Bubble size: `Total Revenue`

### Suggested layout

- Left: region chart
- Right: customer segment chart
- Bottom: top customers table and matrix

## Filters to keep on every page

- `order_year`
- `region`
- `category`
- `customer_segment`
- `sales_channel`

## Design tips

- Keep color meaning consistent:
  - Revenue = blue
  - Profit = green
  - Negative profit = red
- Use clear titles like `Monthly Revenue and Profit` instead of generic `Chart 1`.
- Turn on data labels only where they improve readability.
- Add a text box with 2-3 key findings on each page.

## Minimum visuals to fully answer the project goals

If you want a lean version, build these first:

1. KPI cards
2. Monthly revenue/profit line chart
3. Category revenue bar chart
4. Region revenue bar chart
5. Top customers table
6. Discount analysis chart
7. Promote/review products table

## Final deliverables

When the report is done, save it as:

- `powerbi/retail_sales_dashboard.pbix`

Also export or screenshot these pages for GitHub:

1. Executive Overview
2. Product Performance
3. Customer and Region

