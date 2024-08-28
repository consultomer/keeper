import os
import bcrypt

from Scripts.extensions import mysql


def init_db(app):
    app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
    app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
    app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
    app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")
    app.config["MYSQL_PORT"] = int(os.getenv("MYSQL_PORT", 3306))
    app.config["MYSQL_CURSORCLASS"] = "DictCursor"

    mysql.init_app(app)


def create_users_table():
    query = """
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
    """
    password = "changeme"
    passw = password.encode("utf-8")
    hashed = bcrypt.hashpw(passw, bcrypt.gensalt())
    query2 = """
    INSERT INTO Users (
        name, last_name, username, password, role, status, designation
        ) VALUES (
            %s, %s, %s, %s, %s, 'active', 'none'
            );
    """
    try:

        cur = mysql.connection.cursor()
        cur.execute(query)
        cur.execute(query2, ("Default", "User", "admin", hashed, "admin"))
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        return "User TABLE or User Exists"


def create_customer_table():
    query = """
    CREATE TABLE IF NOT EXISTS Customer (
        customer_id INT PRIMARY KEY AUTO_INCREMENT,
        customer_name VARCHAR(32) NOT NULL,
        customer_email VARCHAR(32) NOT NULL,
        customer_mobile VARCHAR(32) NOT NULL,
        customer_address TEXT,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        created_by INT NOT NULL,
        FOREIGN KEY (created_by) REFERENCES Users(id)
    );
    """
    try:

        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        return "customer Table Already Exists"


def create_employee_table():
    query = """
    CREATE TABLE Employee (
        employee_id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        email VARCHAR(150),
        phone_number VARCHAR(20) NOT NULL,
        status ENUM('Available', 'Not Available') DEFAULT 'Available',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME ON UPDATE CURRENT_TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_by INT NOT NULL,
        FOREIGN KEY (created_by) REFERENCES Users(id)
    );
    """
    try:

        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        return "Deliveryman Table Already Exists"


def create_invoice_table():
    query = """
    CREATE TABLE IF NOT EXISTS Invoice (
        invoice_id INT PRIMARY KEY AUTO_INCREMENT,
        customer_id INT NOT NULL,
        employee_id INT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        invoice_amount INT NOT NULL,
        payment_status VARCHAR(32) DEFAULT 'Pending',
        delivery_status VARCHAR(32) DEFAULT 'Pending',
        notes TEXT,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        created_by INT NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
        FOREIGN KEY (employee_id) REFERENCES Employee(employee_id),
        FOREIGN KEY (created_by) REFERENCES Users(id)
    );
    """
    try:

        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        return "Invoice Table Already Exists"


def create_payment_table():
    query = """
    CREATE TABLE IF NOT EXISTS Payment (
        payment_id INT PRIMARY KEY AUTO_INCREMENT,
        invoice_id INT NOT NULL,
        payment_amount INT NOT NULL,
        payment_method VARCHAR(32) NOT NULL,
        payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        created_by INT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (invoice_id) REFERENCES Invoice(invoice_id),
        FOREIGN KEY (created_by) REFERENCES Users(id)
    );
    """
    try:

        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        return "Payment Table Already Exists"


def create_credit_table():
    query = """
    CREATE TABLE IF NOT EXISTS Credit (
        credit_id INT AUTO_INCREMENT PRIMARY KEY,
        invoice_id INT NOT NULL,
        outstanding_amount INT NOT NULL,
        assigned_to INT,
        recovered_amount INT,
        recovery_date DATETIME,
        FOREIGN KEY (invoice_id) REFERENCES Invoice(invoice_id),
        FOREIGN KEY (assigned_to) REFERENCES Employee(employee_id)
    );
    """
    try:

        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        return "VM_IN Table Already Exists"


def create_orderbooker_table():
    query = """
    CREATE TABLE IF NOT EXISTS OrderBooker (
        orderbooker_id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        phone_number VARCHAR(20) NOT NULL,
        assigned_credit_id INT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME ON UPDATE CURRENT_TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (assigned_credit_id) REFERENCES Invoice(invoice_id)
    );
    """
    try:

        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        return "Orderbooker Table Already Exists"


def create_deliverylog_table():
    query = """
    CREATE TABLE IF NOT EXISTS DeliveryLog (
        log_id INT AUTO_INCREMENT PRIMARY KEY,
        invoice_id INT NOT NULL,
        employee_id INT NOT NULL,
        delivery_status ENUM('Pending', 'Delivered', 'Returned') DEFAULT 'Pending',
        payment_status ENUM('Full Payment', 'Partial Payment', 'No Payment') DEFAULT 'No Payment',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME ON UPDATE CURRENT_TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (invoice_id) REFERENCES Invoice(invoice_id),
        FOREIGN KEY (employee_id) REFERENCES Employee(employee_id)
    );
    """
    try:

        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        return "Deliverylog Table Already Exists"


def create_invoice_adj_table():
    query = """
    CREATE TABLE IF NOT EXISTS InvoiceAdjustment (
        adj_id INT AUTO_INCREMENT PRIMARY KEY,
        invoice_id INT NOT NULL,
        adjustment_type ENUM('Discount', 'Returned') NOT NULL,
        adjustment_amount INT NOT NULL,
        adjustment_reason TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        created_by INT NOT NULL,
        FOREIGN KEY (invoice_id) REFERENCES Invoice(invoice_id),
        FOREIGN KEY (created_by) REFERENCES OrderBooker(orderbooker_id)
    );
    """
    try:

        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        return "Invoice_adj Table Already Exists"
