SELECT
    category,
    ROUND(SUM(net_sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit
FROM retail_sales_view
GROUP BY category
ORDER BY revenue DESC;