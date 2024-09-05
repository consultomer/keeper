from Scripts.extensions import mysql


def add_customer(data):
    query = """
    INSERT INTO Customers (
        business_name, address, area, route, category, phone, whatsapp, shop_ownership, cnic, tax_filer_status, channel, class, business_status, shop_status, business_health
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    );
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            query,
            (
                data["business_name"],
                data["address"],
                data["area"],
                data["route"],
                data["category"],
                data["phone"],
                data["whatsapp"],
                data["shop_ownership"],
                data["cnic"],
                data["tax_filer_status"],
                data["channel"],
                data["class"],
                data["business_status"],
                data["shop_status"],
                data["business_health"],
            ),
        )
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        return f"Error adding Customer: {str(e)}"


def find_customer(cust_id):
    query = "SELECT * FROM Customers WHERE customer_id = %s"
    try:
        cur = mysql.connection.cursor()
        cur.execute(query, (cust_id,))
        data = cur.fetchall()
        cur.close()
        return data if data else None
    except Exception as e:
        return f"Error finding Customer: {str(e)}"


def list_customers(page, per_page):
    offset = (page - 1) * per_page
    query = "SELECT * FROM Customers LIMIT %s OFFSET %s"
    count_query = "SELECT COUNT(*) AS total FROM Customers"

    try:
        cur = mysql.connection.cursor()

        # Fetch paginated results
        cur.execute(query, (per_page, offset))
        data = cur.fetchall()

        # Fetch total count
        cur.execute(count_query)
        total_count = cur.fetchone()["total"]

        cur.close()
        return data, total_count
    except Exception as e:
        print(f"Error fetching customers: {str(e)}")
        return False, 0


def edit_customer(data):
    query = """
    UPDATE Customers SET business_name = %s, address = %s, area = %s, 
    route = %s, category = %s, phone = %s, whatsapp = %s, 
    shop_ownership = %s, cnic = %s, tax_filer_status = %s,
    channel = %s, class = %s, business_status = %s, 
    shop_status = %s, business_health = %s
    WHERE customer_id = %s
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            query,
            (
                data["business_name"],
                data["address"],
                data["area"],
                data["route"],
                data["category"],
                data["phone"],
                data["whatsapp"],
                data["shop_ownership"],
                data["cnic"],
                data["tax_filer_status"],
                data["channel"],
                data["class"],
                data["business_status"],
                data["shop_status"],
                data["business_health"],
                data["customer_id"],
            ),
        )
        affected_rows = cur.rowcount
        mysql.connection.commit()
        cur.close()
        if affected_rows > 0:
            return True
        else:
            return "No matching record found for editing"
    except Exception as e:
        return f"Error editing Customer: {str(e)}"


def delete_customer(customer_id):
    query = "DELETE FROM Customers WHERE customer_id = %s"
    try:
        cur = mysql.connection.cursor()
        cur.execute(query, (customer_id,))
        affected_rows = cur.rowcount
        mysql.connection.commit()
        cur.close()
        if affected_rows > 0:
            return True
        else:
            return "No matching record found for deletion"
    except Exception as e:
        return f"Error deleting Customer: {str(e)}"


def customer():
    query = """
    SELECT customer_id, business_name
    FROM Customers;
    """
    try:
        # Assuming `mysql` is your connection object, replace this with your actual connection method if different
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        print(data)
        return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return False