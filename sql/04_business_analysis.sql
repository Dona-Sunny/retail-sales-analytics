USE retail_sales_analytics;

-- 1. Overall KPIs
SELECT
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers,
    SUM(quantity) AS units_sold,
    ROUND(SUM(net_sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(SUM(profit) / SUM(net_sales) * 100, 2) AS profit_margin_percentage,
    ROUND(SUM(net_sales) / COUNT(DISTINCT order_id), 2) AS average_order_value
FROM retail_sales_view;

-- 2. Monthly sales trend
SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS sales_month,
    ROUND(SUM(net_sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    COUNT(DISTINCT order_id) AS total_orders
FROM retail_sales_view
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY sales_month;

-- 3. Category performance
SELECT
    category,
    ROUND(SUM(net_sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(SUM(profit) / SUM(net_sales) * 100, 2) AS profit_margin_percentage
FROM retail_sales_view
GROUP BY category
ORDER BY revenue DESC;

-- 4. Top-selling products
SELECT
    product_id,
    product_name,
    category,
    SUM(quantity) AS units_sold,
    ROUND(SUM(net_sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit
FROM retail_sales_view
GROUP BY product_id, product_name, category
ORDER BY revenue DESC
LIMIT 10;

-- 5. Regional performance
SELECT
    region,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(net_sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit
FROM retail_sales_view
GROUP BY region
ORDER BY revenue DESC;

-- 6. Top customers
SELECT
    customer_id,
    customer_name,
    customer_segment,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(net_sales), 2) AS customer_revenue,
    ROUND(SUM(profit), 2) AS customer_profit
FROM retail_sales_view
GROUP BY customer_id, customer_name, customer_segment
ORDER BY customer_revenue DESC
LIMIT 10;

-- 7. Customer segmentation
SELECT
    customer_segment,
    COUNT(DISTINCT customer_id) AS total_customers,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(net_sales), 2) AS revenue,
    ROUND(AVG(net_sales), 2) AS average_transaction_value
FROM retail_sales_view
GROUP BY customer_segment
ORDER BY revenue DESC;

-- 8. Discount analysis
SELECT
    CASE
        WHEN discount = 0 THEN 'No Discount'
        WHEN discount <= 0.10 THEN '1-10%'
        WHEN discount <= 0.20 THEN '11-20%'
        ELSE 'Above 20%'
    END AS discount_group,
    ROUND(SUM(net_sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(SUM(profit) / SUM(net_sales) * 100, 2) AS profit_margin_percentage
FROM retail_sales_view
GROUP BY discount_group
ORDER BY revenue DESC;

-- 9. Sales-channel performance
SELECT
    sales_channel,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(net_sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit
FROM retail_sales_view
GROUP BY sales_channel
ORDER BY revenue DESC;

-- 10. Products generating losses
SELECT
    product_name,
    category,
    ROUND(SUM(net_sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit
FROM retail_sales_view
GROUP BY product_name, category
HAVING SUM(profit) < 0
ORDER BY profit;

-- 11. Products to promote
SELECT
    product_name,
    category,
    ROUND(SUM(net_sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(SUM(profit) / SUM(net_sales) * 100, 2) AS profit_margin_percentage
FROM retail_sales_view
GROUP BY product_name, category
HAVING SUM(profit) > 0
ORDER BY profit DESC
LIMIT 10;

-- 12. Products to review
SELECT
    product_name,
    category,
    ROUND(SUM(net_sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(SUM(profit) / SUM(net_sales) * 100, 2) AS profit_margin_percentage
FROM retail_sales_view
GROUP BY product_name, category
HAVING SUM(profit) < 0
   OR SUM(profit) / NULLIF(SUM(net_sales), 0) < 0.10
ORDER BY profit ASC, revenue DESC
LIMIT 15;

