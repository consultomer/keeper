from Scripts.extensions import mysql


def add_invoice(data):
    query = """
    INSERT INTO Invoice (
        customer_id, invoice_amount, payment_status, delivery_status, delivery_id, notes, created_by
    ) VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            query,
            (
                data["customer_id"],
                data["invoice_amount"],
                data["payment_status"],
                data["delivery_status"],
                data["delivery_id"],
                data["notes"],
                data["created_by"],
            ),
        )
        mysql.connection.commit()
        cur.close()
        return "Invoice Added Successfully", 200
    except Exception as e:
        return f"Error adding Invoice: {str(e)}", 400


def list_invoices():
    query = "SELECT * FROM Invoice"
    try:
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        return data
    except Exception as e:
        return False


def edit_invoice(data):
    query = """
    UPDATE Invoice SET invoice_amount = %s, payment_status = %s, 
    delivery_status = %s, delivery_id = %s, notes = %s, updated_at = CURRENT_TIMESTAMP 
    WHERE invoice_id = %s
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            query,
            (
                data["invoice_amount"],
                data["payment_status"],
                data["delivery_status"],
                data["delivery_id"],
                data["notes"],
                data["invoice_id"],
            ),
        )
        affected_rows = cur.rowcount
        mysql.connection.commit()
        cur.close()
        return (
            "Invoice Edited Successfully",
            200 if affected_rows > 0 else "No matching record found for editing",
            404,
        )
    except Exception as e:
        return f"Error editing Invoice: {str(e)}", 400


def delete_invoice(invoice_id):
    query = "DELETE FROM Invoice WHERE invoice_id = %s"
    try:
        cur = mysql.connection.cursor()
        cur.execute(query, (invoice_id,))
        affected_rows = cur.rowcount
        mysql.connection.commit()
        cur.close()
        return (
            "Invoice Deleted Successfully",
            200 if affected_rows > 0 else "No matching record found for deletion",
            404,
        )
    except Exception as e:
        return f"Error deleting Invoice: {str(e)}", 400
