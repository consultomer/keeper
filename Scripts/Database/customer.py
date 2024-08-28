from Scripts.extensions import mysql


def add_customer(data):
    query = """
    INSERT INTO Customer (
        customer_name, customer_email, customer_mobile, customer_address, created_by
        ) VALUES (%s, %s, %s, %s, %s);
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            query,
            (
                data["customer_name"],
                data["customer_email"],
                data["customer_mobile"],
                data["customer_address"],
                data["created_by"],
            ),
        )
        mysql.connection.commit()
        cur.close()
        return "Customer Added Successfully", 200
    except Exception as e:
        return f"Error adding Customer: {str(e)}", 400


def list_customers():
    query = "SELECT * FROM Customer"
    try:
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        return data
    except Exception as e:
        return f"Error listing Customers: {str(e)}"


def edit_customer(data):
    query = """
    UPDATE Customer SET customer_name = %s, customer_email = %s, 
    customer_mobile = %s, customer_address = %s, updated_at = CURRENT_TIMESTAMP 
    WHERE customer_id = %s
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            query,
            (
                data["customer_name"],
                data["customer_email"],
                data["customer_mobile"],
                data["customer_address"],
                data["customer_id"],
            ),
        )
        affected_rows = cur.rowcount
        mysql.connection.commit()
        cur.close()
        return (
            "Customer Edited Successfully",
            200 if affected_rows > 0 else "No matching record found for editing",
            404,
        )
    except Exception as e:
        return f"Error editing Customer: {str(e)}", 400


def delete_customer(customer_id):
    query = "DELETE FROM Customer WHERE customer_id = %s"
    try:
        cur = mysql.connection.cursor()
        cur.execute(query, (customer_id,))
        affected_rows = cur.rowcount
        mysql.connection.commit()
        cur.close()
        return (
            "Customer Deleted Successfully",
            200 if affected_rows > 0 else "No matching record found for deletion",
            404,
        )
    except Exception as e:
        return f"Error deleting Customer: {str(e)}", 400
