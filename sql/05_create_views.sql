USE retail_sales_analytics;

DROP VIEW IF EXISTS retail_sales_view;
DROP VIEW IF EXISTS customer_lifetime_value_view;
DROP VIEW IF EXISTS product_profitability_view;

CREATE VIEW retail_sales_view AS
SELECT
    o.order_id,
    o.order_date,
    YEAR(o.order_date) AS order_year,
    MONTH(o.order_date) AS order_month_number,
    MONTHNAME(o.order_date) AS order_month,
    c.customer_id,
    c.customer_name,
    c.customer_segment,
    c.city,
    c.province,
    c.region,
    p.product_id,
    p.product_name,
    p.category,
    p.subcategory,
    oi.quantity,
    oi.unit_price,
    p.cost_per_unit,
    oi.discount,
    o.sales_channel,
    o.payment_method,
    oi.quantity * oi.unit_price AS gross_sales,
    oi.quantity * oi.unit_price * oi.discount AS discount_amount,
    oi.quantity * oi.unit_price * (1 - oi.discount) AS net_sales,
    oi.quantity * p.cost_per_unit AS total_cost,
    (oi.quantity * oi.unit_price * (1 - oi.discount))
        - (oi.quantity * p.cost_per_unit) AS profit
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
JOIN products p
    ON oi.product_id = p.product_id;

CREATE VIEW customer_lifetime_value_view AS
SELECT
    customer_id,
    customer_name,
    customer_segment,
    region,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(net_sales), 2) AS lifetime_revenue,
    ROUND(SUM(profit), 2) AS lifetime_profit,
    ROUND(AVG(net_sales), 2) AS average_transaction_value
FROM retail_sales_view
GROUP BY customer_id, customer_name, customer_segment, region;

CREATE VIEW product_profitability_view AS
SELECT
    product_id,
    product_name,
    category,
    subcategory,
    SUM(quantity) AS units_sold,
    ROUND(SUM(net_sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(SUM(profit) / NULLIF(SUM(net_sales), 0) * 100, 2) AS profit_margin_percentage
FROM retail_sales_view
GROUP BY product_id, product_name, category, subcategory;

-- Quick test
SELECT *
FROM retail_sales_view
LIMIT 20;

