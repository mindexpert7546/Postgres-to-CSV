CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    price NUMERIC(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id INT,
    product_id INT,
    quantity INT,
    order_date DATE,
    CONSTRAINT fk_user
        FOREIGN KEY (user_id) REFERENCES users(user_id),
    CONSTRAINT fk_product
        FOREIGN KEY (product_id) REFERENCES products(product_id)
);

INSERT INTO users (full_name, email)
VALUES
('Abhinav Singh', 'abhinav@gmail.com'),
('Rahul Sharma', 'rahul@gmail.com'),
('Priya Verma', 'priya@gmail.com');

INSERT INTO products (product_name, price)
VALUES
('Laptop', 55000.00),
('Mobile Phone', 22000.00),
('Headphones', 2500.00);

INSERT INTO orders (user_id, product_id, quantity, order_date)
VALUES
(1, 1, 1, '2026-01-15'),
(2, 2, 2, '2026-01-16'),
(3, 3, 1, '2026-01-17');


SELECT full_name, email FROM users;
SELECT product_name,price FROM products;
SELECT user_id, product_id, quantity, order_date from orders;
