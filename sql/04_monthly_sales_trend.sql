SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS sales_month,
    ROUND(SUM(net_sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit
FROM retail_sales_view
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY sales_month;