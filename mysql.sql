create database Keeper;
use Keeper;
-- Create Users Table
CREATE TABLE IF NOT EXISTS Users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(32) NOT NULL,
    last_name VARCHAR(32) NOT NULL,
    username VARCHAR(32) NOT NULL UNIQUE,
    password VARCHAR(120) NOT NULL,
    role VARCHAR(32) NOT NULL,
    status VARCHAR(32) NOT NULL,
    designation VARCHAR(32) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Customers Table
CREATE TABLE IF NOT EXISTS Customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    business_name VARCHAR(255) NOT NULL UNIQUE,
    address VARCHAR(255) NOT NULL,
    area VARCHAR(100),
    route VARCHAR(100),
    category VARCHAR(100),
    phone VARCHAR(20),
    whatsapp VARCHAR(20),
    shop_ownership ENUM('Yes', 'No') NOT NULL,
    cnic VARCHAR(15),
    tax_filer_status ENUM('Filer', 'Non Filer') NOT NULL,
    channel VARCHAR(100),
    class VARCHAR(100),
    business_status ENUM('Active', 'Inactive') NOT NULL,
    shop_status ENUM('Active', 'Inactive') NOT NULL,
    business_health ENUM('Gold', 'Platinum', 'Silver', 'Defaulter', 'Blacklist') NOT NULL
);

-- Create Employee Table
CREATE TABLE IF NOT EXISTS Employee (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    role ENUM('Booker', 'Delivery Man'),
    phone_number VARCHAR(20) NOT NULL,
    whatsapp_number VARCHAR(20),
    address VARCHAR(255) NOT NULL,
    company ENUM('CP', 'RB', 'JR', 'GP', 'Other')
);

-- Create Invoice Table
CREATE TABLE IF NOT EXISTS Invoice (
    invoice_id INT PRIMARY KEY AUTO_INCREMENT,
    booker INT NOT NULL,
    delivery_man INT NULL,
    dsr VARCHAR(255),
    customer_id INT NOT NULL,
    total DECIMAL(25, 0) DEFAULT 0,
    paid DECIMAL(25, 0) DEFAULT 0,
    company VARCHAR(255),
    revision DECIMAL(25, 0) DEFAULT 0,
    delivery_status ENUM('Un-delivered', 'Delivered', 'Returned', 'Processing') DEFAULT 'Un-delivered',
    payment_status ENUM('Full Payment', 'Partial Payment', 'No Payment') DEFAULT 'No Payment',
    notes TEXT DEFAULT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (booker) REFERENCES Employee(employee_id),
    FOREIGN KEY (delivery_man) REFERENCES Employee(employee_id)
);

-- Create Dispatch Table
CREATE TABLE IF NOT EXISTS Dispatch (
    dispatch_id INT PRIMARY KEY AUTO_INCREMENT,
    delivery_man INT NOT NULL,
    dispatch_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (delivery_man) REFERENCES Employee(employee_id)
);

-- Create DispatchInvoice Table
CREATE TABLE IF NOT EXISTS DispatchInvoice (
    dispatch_invoice_id INT PRIMARY KEY AUTO_INCREMENT,
    dispatch_id INT NOT NULL,
    invoice_id INT NOT NULL,
    FOREIGN KEY (dispatch_id) REFERENCES Dispatch(dispatch_id),
    FOREIGN KEY (invoice_id) REFERENCES Invoice(invoice_id)
);

