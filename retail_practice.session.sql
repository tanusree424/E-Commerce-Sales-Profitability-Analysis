SELECT COUNT(DISTINCT order_id)
 AS total_orders FROM cleaned_ecom_data;


SELECT ROUND(SUM(net_sales),2)
 AS total_sales FROM cleaned_ecom_data;

-- Gross Sales
SELECT ROUND(SUM(gross_sales),2)
 AS total_sales FROM cleaned_ecom_data;

-- Total Profit 
SELECT ROUND(SUM(profit),2) AS total_profit 
FROM cleaned_ecom_data;

-- Quantity Sold
SELECT SUM(quantity) AS total_quantity_sold 
FROM cleaned_ecom_data;

-- Total Cost
SELECT Round(SUM(cost),2) AS total_cost
FROM cleaned_ecom_data;
-- Profit Margin
SELECT SUM(profit) as Total_profit , SUM(net_sales) AS total_sales, ROUND((SUM(profit) / SUM(net_sales)),2) AS profit_margin FROM cleaned_ecom_data;
-- Order Avarage Value
SELECT COUNT(DISTINCT order_id) AS total_orders , 
SUM(net_sales) AS total_sales ,
 ROUND((SUM(net_sales)  / COUNT(DISTINCT order_id)),2) AS Avarage_order_value
 FROM cleaned_ecom_data;

-- Total Returned Items
SELECT COUNT(DISTINCT order_item_id) AS total_orders_items 
FROM cleaned_ecom_data WHERE returned = 1;

-- Return Rate
SELECT
   
    ROUND(
        COUNT(DISTINCT CASE
            WHEN returned = 1 THEN order_item_id
        END) * 100.0 /
        NULLIF(COUNT(DISTINCT order_item_id), 0),
        2
    ) AS return_rate

FROM cleaned_ecom_data;

-- Non Return Item
SELECT COUNT(DISTINCT order_id) AS Non_return_items 
FROM cleaned_ecom_data WHERE returned = 0;
-- Total discount
SELECT gross_sales , net_sales , 
Round(SUM((gross_sales - net_sales)),2) AS discount  
FROM cleaned_ecom_data;
-- Avarage Discount
SELECT ROUND(AVG(discount),2) AS Avarage_discount 
FROM cleaned_ecom_data;

-- Total Customers
SELECT COUNT(DISTINCT customer_id) AS total_customers FROM cleaned_ecom_data;

-- Unknown customer
SELECT COUNT(*) AS total_unknown_customer
 FROM cleaned_ecom_data WHERE customer_unknown =1;

SELECT order_date, MAX(order_date) AS latest_order_date , MIN(order_date) AS first_date FROM cleaned_ecom_data;