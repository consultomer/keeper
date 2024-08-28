from Scripts.extensions import mysql


def add_payment(data):
    query = """
    INSERT INTO Payment (
        invoice_id, payment_amount, payment_method, created_by
    ) VALUES (%s, %s, %s, %s);
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            query,
            (
                data["invoice_id"],
                data["payment_amount"],
                data["payment_method"],
                data["created_by"],
            ),
        )
        mysql.connection.commit()
        cur.close()
        return "Payment Added Successfully", 200
    except Exception as e:
        return f"Error adding Payment: {str(e)}", 400


def list_payments():
    query = "SELECT * FROM Payment"
    try:
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        return data
    except Exception as e:
        return f"Error listing Payments: {str(e)}"


def edit_payment(data):
    query = """
    UPDATE Payment SET payment_amount = %s, payment_method = %s, 
    updated_at = CURRENT_TIMESTAMP WHERE payment_id = %s
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            query, (data["payment_amount"], data["payment_method"], data["payment_id"])
        )
        affected_rows = cur.rowcount
        mysql.connection.commit()
        cur.close()
        return (
            "Payment Edited Successfully",
            200 if affected_rows > 0 else "No matching record found for editing",
            404,
        )
    except Exception as e:
        return f"Error editing Payment: {str(e)}", 400


def delete_payment(payment_id):
    query = "DELETE FROM Payment WHERE payment_id = %s"
    try:
        cur = mysql.connection.cursor()
        cur.execute(query, (payment_id,))
        affected_rows = cur.rowcount
        mysql.connection.commit()
        cur.close()
        return (
            "Payment Deleted Successfully",
            200 if affected_rows > 0 else "No matching record found for deletion",
            404,
        )
    except Exception as e:
        return f"Error deleting Payment: {str(e)}", 400
