from Scripts.extensions import mysql


def add_invoice(data):
    query = """
    INSERT INTO Invoice (
        booker, delivery_man, dsr, customer_id, total, company
    ) VALUES (%s, %s, %s, %s, %s, %s);
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            query,
            (
                data["booker"],
                data["delivery_man"],
                data["dsr"],
                data["customer_id"],
                data["total"],
                data["company"],
            ),
        )
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        return f"Error adding Invoice: {str(e)}"


def list_invoices():
    query = """
    SELECT 
        i.invoice_id,
        e1.name AS booker_name,
        e2.name AS delivery_man,
        i.dsr,
        c.business_name AS customer_name,
        i.total,
        i.company,
        i.revision,
        i.delivery_status,
        i.payment_status,
        i.notes,
        DATE(i.created_at) AS created_at,
        DATEDIFF(CURDATE(), i.created_at) AS age
    FROM Invoice i
    JOIN Employee e1 ON i.booker = e1.employee_id
    JOIN Employee e2 ON i.delivery_man = e2.employee_id
    JOIN Customers c ON i.customer_id = c.customer_id;
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        return data
    except Exception as e:
        return False


def single_invoice(value):
    query = "SELECT * FROM Invoice WHERE invoice_id = %s"
    try:
        cur = mysql.connection.cursor()
        cur.execute(query, (value,))
        data = cur.fetchall()
        cur.close()
        return data if data else None
    except Exception as e:
        return f"Error finding Customer: {str(e)}"


def edit_invoice(data):
    query = """
        UPDATE Invoice 
        SET booker = %s, delivery_man = %s, dsr = %s, customer_id = %s, total = %s, paid = %s, company = %s, revision = %s, delivery_status = %s, payment_status = %s, notes = %s
        WHERE invoice_id = %s
        """
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            query,
            (
                data["booker"],
                data["delivery_man"],
                data["dsr"],
                data["customer_id"],
                data["total"],
                data["paid"],
                data["company"],
                data["revision"],
                data["delivery_status"],
                data["payment_status"],
                data["notes"],
                data["invoice_id"],
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
        return f"Error editing Invoice: {str(e)}"


def delete_invoice(invoice_id):
    query = "DELETE FROM Invoice WHERE invoice_id = %s"
    try:
        cur = mysql.connection.cursor()
        cur.execute(query, (invoice_id,))
        affected_rows = cur.rowcount
        mysql.connection.commit()
        cur.close()
        if affected_rows > 0:
            return True
        else:
            return "No Matching Record Found"
    except Exception as e:
        return f"Error deleting Invoice: {str(e)}"


def sininvoice(value):
    query = """
    SELECT 
        i.invoice_id,
        e1.name AS booker_name,
        e2.name AS delivery_man,
        i.dsr,
        c.business_name AS customer_name,
        c.address AS customer_add,
        c.phone AS customer_phone,
        i.total,
        i.paid,
        i.company,
        i.revision,
        i.delivery_status,
        i.payment_status,
        i.notes,
        DATE(i.created_at) AS created_at,
        DATEDIFF(CURDATE(), i.created_at) AS age
    FROM Invoice i
    JOIN Employee e1 ON i.booker = e1.employee_id
    JOIN Employee e2 ON i.delivery_man = e2.employee_id
    JOIN Customers c ON i.customer_id = c.customer_id
    WHERE i.invoice_id = %s;
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute(query, (value,))
        data = cur.fetchall()
        cur.close()
        return data
    except Exception as e:
        return False