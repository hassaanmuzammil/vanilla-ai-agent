-- Insert 10 customers
INSERT INTO customers (name, email, phone, address) VALUES
('Alice Smith', 'alice@example.com', '1234567890', '123 Main St'),
('Bob Johnson', 'bob@example.com', '2345678901', '456 Elm St'),
('Carol Davis', 'carol@example.com', '3456789012', '789 Oak St'),
('David Wilson', 'david@example.com', '4567890123', '101 Maple St'),
('Emma Brown', 'emma@example.com', '5678901234', '202 Pine St'),
('Frank Thomas', 'frank@example.com', '6789012345', '303 Cedar St'),
('Grace Lee', 'grace@example.com', '7890123456', '404 Birch St'),
('Henry Martin', 'henry@example.com', '8901234567', '505 Walnut St'),
('Isabel Clark', 'isabel@example.com', '9012345678', '606 Spruce St'),
('Jack Turner', 'jack@example.com', '0123456789', '707 Chestnut St');

-- Insert 10 products
INSERT INTO products (name, description, price, stock_quantity) VALUES
('Laptop', 'High performance laptop', 1200.00, 50),
('Smartphone', 'Latest model smartphone', 800.00, 100),
('Headphones', 'Noise cancelling headphones', 150.00, 200),
('Keyboard', 'Mechanical keyboard', 90.00, 150),
('Mouse', 'Wireless mouse', 40.00, 180),
('Monitor', '24-inch full HD monitor', 200.00, 75),
('Tablet', '10-inch Android tablet', 300.00, 80),
('Charger', 'Fast charging USB-C charger', 25.00, 300),
('Webcam', '1080p HD webcam', 60.00, 100),
('Microphone', 'USB condenser microphone', 110.00, 70);

-- Generate 100 orders with random customer assignments
DO $$
BEGIN
    FOR i IN 1..100 LOOP
        INSERT INTO orders (customer_id, order_date, status)
        VALUES (
            (SELECT id FROM customers ORDER BY random() LIMIT 1),
            CURRENT_DATE - (random() * 30)::int,
            (ARRAY['pending', 'shipped', 'delivered', 'canceled'])[floor(random() * 4 + 1)]
        );
    END LOOP;
END$$;

-- Add 1 to 5 items to each order
DO $$
DECLARE
    order_id INT;
    num_items INT;
    i INT;
    product_id INT;
    quantity INT;
    price NUMERIC;
BEGIN
    FOR order_row IN SELECT id FROM orders LOOP
        num_items := floor(random() * 5 + 1);
        FOR i IN 1..num_items LOOP
            product_id := (SELECT id FROM products ORDER BY random() LIMIT 1);
            quantity := floor(random() * 3 + 1);
            price := (SELECT price FROM products WHERE id = product_id);
            
            INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase)
            VALUES (order_row.id, product_id, quantity, price);
        END LOOP;
    END LOOP;
END$$;
