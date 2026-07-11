USE retail_sales_analytics;

-- Row counts
SELECT COUNT(*) AS total_customers
FROM customers;

SELECT COUNT(*) AS total_products
FROM products;

SELECT COUNT(*) AS total_orders
FROM orders;

SELECT COUNT(*) AS total_order_items
FROM order_items;

-- Missing values
SELECT *
FROM customers
WHERE customer_id IS NULL
   OR customer_name IS NULL;

SELECT *
FROM products
WHERE product_id IS NULL
   OR product_name IS NULL;

SELECT *
FROM orders
WHERE order_id IS NULL
   OR customer_id IS NULL
   OR order_date IS NULL;

-- Invalid numeric values
SELECT *
FROM order_items
WHERE quantity <= 0;

SELECT *
FROM order_items
WHERE unit_price <= 0;

SELECT *
FROM order_items
WHERE discount < 0
   OR discount > 1;

-- Duplicate order-product combinations
SELECT
    order_id,
    product_id,
    COUNT(*) AS duplicate_count
FROM order_items
GROUP BY order_id, product_id
HAVING COUNT(*) > 1;

-- Orphan checks
SELECT o.*
FROM orders o
LEFT JOIN customers c
    ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

SELECT oi.*
FROM order_items oi
LEFT JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.order_id IS NULL;

SELECT oi.*
FROM order_items oi
LEFT JOIN products p
    ON oi.product_id = p.product_id
WHERE p.product_id IS NULL;

-- Coverage checks
SELECT
    MIN(order_date) AS first_order_date,
    MAX(order_date) AS last_order_date
FROM orders;

SELECT
    c.region,
    COUNT(DISTINCT o.order_id) AS orders_in_region
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.region
ORDER BY orders_in_region DESC;

