USE retail_sales_analytics;

SELECT *
FROM order_items
WHERE quantity <= 0;

SELECT *
FROM order_items
WHERE discount < 0 OR discount > 1;

SELECT
    order_id,
    product_id,
    COUNT(*) AS duplicate_count
FROM order_items
GROUP BY order_id, product_id
HAVING COUNT(*) > 1;