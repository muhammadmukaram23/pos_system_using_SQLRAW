-- Create database
CREATE DATABASE IF NOT EXISTS pos_system;
USE pos_system;

-- Product Category Table
CREATE TABLE IF NOT EXISTS tblproductcategory (
    category_id INT(11) AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(25)
);

-- Product Unit Table
CREATE TABLE IF NOT EXISTS tblproductunit (
    unit_id INT(11) AUTO_INCREMENT PRIMARY KEY,
    unit_name VARCHAR(15)
);

-- User Table
CREATE TABLE IF NOT EXISTS tbluser (
    user_id INT(11) AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(30) UNIQUE,
    password VARCHAR(30),
    fullname VARCHAR(50),
    designation INT(1),
    contact VARCHAR(15),
    account_type INT(1)
);

-- Product Table
CREATE TABLE IF NOT EXISTS tblproduct (
    product_id INT(11) AUTO_INCREMENT PRIMARY KEY,
    produce_code VARCHAR(25),
    product_name VARCHAR(50),
    unit_id INT(11),
    category_id INT(11),
    unit_in_stock FLOAT,
    unit_price FLOAT,
    discount_percentage FLOAT,
    reorder_level FLOAT,
    user_id INT(11),
    FOREIGN KEY (unit_id) REFERENCES tblproductunit(unit_id),
    FOREIGN KEY (category_id) REFERENCES tblproductcategory(category_id),
    FOREIGN KEY (user_id) REFERENCES tbluser(user_id)
);

-- Customer Table
CREATE TABLE IF NOT EXISTS tblcustomer (
    customer_id INT(11) AUTO_INCREMENT PRIMARY KEY,
    customer_code VARCHAR(25),
    customer_name VARCHAR(50),
    contact VARCHAR(15),
    address VARCHAR(100)
);

-- Supplier Table
CREATE TABLE IF NOT EXISTS tblsupplier (
    supplier_id INT(11) AUTO_INCREMENT PRIMARY KEY,
    supplier_code VARCHAR(15),
    supplier_name VARCHAR(50),
    supplier_contact VARCHAR(15),
    supplier_address VARCHAR(100),
    supplier_email VARCHAR(50),
    contact_person VARCHAR(50),
    bank_account_name VARCHAR(50),
    bank_account_number VARCHAR(25)
);

-- Invoice Table
CREATE TABLE IF NOT EXISTS tblinvoice (
    invoice_id INT(11) AUTO_INCREMENT PRIMARY KEY,
    customer_id INT(11),
    payment_type INT(1),
    total_amount FLOAT,
    amount_tendered FLOAT,
    bank_account_name VARCHAR(50),
    bank_account_number VARCHAR(25),
    date_recorded DATE,
    user_id INT(11),
    FOREIGN KEY (customer_id) REFERENCES tblcustomer(customer_id),
    FOREIGN KEY (user_id) REFERENCES tbluser(user_id)
);

-- Sales Table
CREATE TABLE IF NOT EXISTS tblsales (
    sales_id INT(11) AUTO_INCREMENT PRIMARY KEY,
    invoice_id INT(11),
    product_id INT(11),
    quantity FLOAT,
    unit_price FLOAT,
    sub_total FLOAT,
    FOREIGN KEY (invoice_id) REFERENCES tblinvoice(invoice_id),
    FOREIGN KEY (product_id) REFERENCES tblproduct(product_id)
);

-- Receive Product Table
CREATE TABLE IF NOT EXISTS tblreceiveproduct (
    receive_product_id INT(11) AUTO_INCREMENT PRIMARY KEY,
    product_id INT(11),
    quantity FLOAT,
    unit_price FLOAT,
    sub_total FLOAT,
    supplier_id INT(11),
    received_date DATE,
    user_id INT(11),
    purchase_order_id INT(11) NULL,
    FOREIGN KEY (product_id) REFERENCES tblproduct(product_id),
    FOREIGN KEY (supplier_id) REFERENCES tblsupplier(supplier_id),
    FOREIGN KEY (user_id) REFERENCES tbluser(user_id)
);

-- Purchase Order Table
CREATE TABLE IF NOT EXISTS tblpurchaseorder (
    purchase_order_id INT(11) AUTO_INCREMENT PRIMARY KEY,
    product_id INT(11),
    quantity FLOAT,
    unit_price FLOAT,
    sub_total FLOAT,
    supplier_id INT(11),
    order_date DATE,
    user_id INT(11),
    status VARCHAR(20) DEFAULT 'pending',
    FOREIGN KEY (product_id) REFERENCES tblproduct(product_id),
    FOREIGN KEY (supplier_id) REFERENCES tblsupplier(supplier_id),
    FOREIGN KEY (user_id) REFERENCES tbluser(user_id)
);

-- Insert sample data for testing
-- Product Categories
INSERT INTO tblproductcategory (category_name) VALUES 
('Electronics'),
('Furniture'),
('Office Supplies'),
('Groceries'),
('Clothing');

-- Product Units
INSERT INTO tblproductunit (unit_name) VALUES 
('Piece'),
('Kg'),
('Liter'),
('Pack'),
('Dozen');

-- Users (Default password: password123)
INSERT INTO tbluser (username, password, fullname, designation, contact, account_type) VALUES 
('admin', 'password123', 'System Administrator', 1, '123-456-7890', 1),
('cashier1', 'password123', 'John Doe', 2, '123-456-7891', 2),
('manager1', 'password123', 'Jane Smith', 3, '123-456-7892', 3);

-- Suppliers
INSERT INTO tblsupplier (supplier_code, supplier_name, supplier_contact, supplier_address, supplier_email, contact_person, bank_account_name, bank_account_number) VALUES 
('SUP001', 'ABC Electronics', '555-123-4567', '123 Main St, City', 'contact@abcelectronics.com', 'John Smith', 'ABC Electronics Bank Account', '1234567890'),
('SUP002', 'XYZ Furniture', '555-234-5678', '456 Oak St, Town', 'sales@xyzfurniture.com', 'Sarah Johnson', 'XYZ Furniture Bank Account', '2345678901'),
('SUP003', 'Office World', '555-345-6789', '789 Pine St, Village', 'info@officeworld.com', 'Mike Davis', 'Office World Bank Account', '3456789012');

-- Customers
INSERT INTO tblcustomer (customer_code, customer_name, contact, address) VALUES 
('CUST001', 'Retail Customer', 'Walk-in', 'N/A'),
('CUST002', 'Corporation Inc.', '555-987-6543', '987 Corp Blvd, Business Park'),
('CUST003', 'School District', '555-876-5432', '654 Education Ave, Learning Center');