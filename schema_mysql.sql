-- Retail Practice Dataset — MySQL 8.0+
-- Part A: staging tables (raw CSV যেমন আছে তেমন লোড করার জন্য, সব VARCHAR)
-- Part B: clean target tables (cleaning এর পরে লোড করার জন্য, constraint সহ)

CREATE DATABASE IF NOT EXISTS retail_practice
  CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE retail_practice;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS order_items, orders, products, customers;
DROP TABLE IF EXISTS stg_customers, stg_products, stg_orders, stg_order_items;
SET FOREIGN_KEY_CHECKS = 1;

-- ─────────────── Part A: STAGING (raw) ───────────────
CREATE TABLE stg_customers (
  customer_id VARCHAR(255), customer_name VARCHAR(255), email VARCHAR(255), segment VARCHAR(255),
  signup_date VARCHAR(255), city VARCHAR(255), region VARCHAR(255), country VARCHAR(255)
);
CREATE TABLE stg_products (
  product_id VARCHAR(255), product_name VARCHAR(255), category VARCHAR(255), subcategory VARCHAR(255),
  unit_cost VARCHAR(255), list_price VARCHAR(255)
);
CREATE TABLE stg_orders (
  order_id VARCHAR(255), customer_id VARCHAR(255), order_date VARCHAR(255), ship_date VARCHAR(255),
  status VARCHAR(255), region VARCHAR(255), ship_mode VARCHAR(255), shipping_cost VARCHAR(255),
  payment_method VARCHAR(255)
);
CREATE TABLE stg_order_items (
  order_item_id VARCHAR(255), order_id VARCHAR(255), product_id VARCHAR(255), quantity VARCHAR(255),
  unit_price VARCHAR(255), discount VARCHAR(255), cost VARCHAR(255), profit VARCHAR(255),
  returned VARCHAR(255), return_reason VARCHAR(255)
);

-- লোড করার উদাহরণ (local_infile চালু থাকতে হবে; path নিজের মতো বদলাও):
-- LOAD DATA LOCAL INFILE '/path/to/orders.csv' INTO TABLE stg_orders
--   FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;
-- খালি field NULL হয় না, '' হিসেবে ঢোকে; NULLIF(col, '') ব্যবহার করো।

-- ─────────────── Part B: CLEAN TARGET ───────────────
CREATE TABLE customers (
  customer_id   VARCHAR(10)  NOT NULL,
  customer_name VARCHAR(100) NOT NULL,
  email         VARCHAR(150),
  segment       ENUM('Consumer','Corporate','Home Office') NOT NULL,
  signup_date   DATE,
  city          VARCHAR(60),
  region        VARCHAR(30),
  country       VARCHAR(30) NOT NULL DEFAULT 'Bangladesh',
  PRIMARY KEY (customer_id),
  UNIQUE KEY uq_customers_email (email)
);

CREATE TABLE products (
  product_id   VARCHAR(10)  NOT NULL,
  product_name VARCHAR(120) NOT NULL,
  category     VARCHAR(40)  NOT NULL,
  subcategory  VARCHAR(40),
  unit_cost    DECIMAL(12,2) NOT NULL,
  list_price   DECIMAL(12,2) NOT NULL,
  PRIMARY KEY (product_id),
  UNIQUE KEY uq_products_name (product_name),
  CONSTRAINT chk_products_cost CHECK (unit_cost >= 0 AND list_price >= unit_cost)
);

CREATE TABLE orders (
  order_id       VARCHAR(15) NOT NULL,
  customer_id    VARCHAR(10) NOT NULL,
  order_date     DATE        NOT NULL,
  ship_date      DATE,
  status         ENUM('Delivered','Shipped','Processing','Cancelled') NOT NULL,
  region         VARCHAR(30),
  ship_mode      ENUM('Standard','Express','Same Day') NOT NULL,
  shipping_cost  DECIMAL(10,2) NOT NULL,
  payment_method VARCHAR(30),
  PRIMARY KEY (order_id),
  KEY idx_orders_customer (customer_id),
  KEY idx_orders_date (order_date),
  CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
  CONSTRAINT chk_orders_ship CHECK (ship_date IS NULL OR ship_date >= order_date),
  CONSTRAINT chk_orders_shipcost CHECK (shipping_cost >= 0)
);

CREATE TABLE order_items (
  order_item_id VARCHAR(15) NOT NULL,
  order_id      VARCHAR(15) NOT NULL,
  product_id    VARCHAR(10) NOT NULL,
  quantity      INT         NOT NULL,
  unit_price    DECIMAL(12,2) NOT NULL,
  discount      DECIMAL(4,3)  NOT NULL DEFAULT 0,
  cost          DECIMAL(14,2) NOT NULL,
  profit        DECIMAL(14,2) NOT NULL,
  returned      TINYINT(1)  NOT NULL DEFAULT 0,
  return_reason VARCHAR(40),
  PRIMARY KEY (order_item_id),
  UNIQUE KEY uq_order_product (order_id, product_id),
  KEY idx_items_product (product_id),
  CONSTRAINT fk_items_order   FOREIGN KEY (order_id)   REFERENCES orders (order_id),
  CONSTRAINT fk_items_product FOREIGN KEY (product_id) REFERENCES products (product_id),
  CONSTRAINT chk_items_qty  CHECK (quantity > 0),
  CONSTRAINT chk_items_disc CHECK (discount BETWEEN 0 AND 0.30),
  CONSTRAINT chk_items_ret  CHECK (returned = 1 OR return_reason IS NULL)
);

-- ─────────────── Metric view (clean data লোড হলে) ───────────────
CREATE OR REPLACE VIEW v_item_metrics AS
SELECT oi.order_item_id, o.order_id, o.customer_id, o.order_date, o.region, p.category, p.subcategory,
       oi.quantity * oi.unit_price                         AS gross_sales,
       oi.quantity * oi.unit_price * (1 - oi.discount)     AS net_sales,
       oi.cost,
       oi.quantity * oi.unit_price * (1 - oi.discount) - oi.cost AS profit_calc,
       oi.returned
FROM order_items oi
JOIN orders   o ON o.order_id   = oi.order_id
JOIN products p ON p.product_id = oi.product_id
WHERE o.status <> 'Cancelled';
