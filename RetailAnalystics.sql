CREATE DATABASE retail_sales_analytics;
USE retail_sales_analytics;
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    gender VARCHAR(10),
    city VARCHAR(50),
    province VARCHAR(50),
    join_date DATE
);
SHOW TABLES;
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    unit_price DECIMAL(10,2)
);
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    region VARCHAR(50),

    FOREIGN KEY (customer_id)
    REFERENCES customers(customer_id)
);
CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    sales_price DECIMAL(10,2),

    FOREIGN KEY (order_id)
    REFERENCES orders(order_id),

    FOREIGN KEY (product_id)
    REFERENCES products(product_id)
);
SHOW TABLES;
DESCRIBE customers;
DESCRIBE products;
DESCRIBE orders;
DESCRIBE order_items;
INSERT INTO customers
VALUES
(1,'John','Smith','Male','Toronto','Ontario','2023-01-12'),
(2,'Sarah','Brown','Female','Ottawa','Ontario','2023-03-18'),
(3,'David','Lee','Male','Vancouver','British Columbia','2024-02-10');

SELECT *
FROM customers;