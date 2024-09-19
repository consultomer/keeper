from Scripts.extensions import mysql


def add_invoice(data):
    query = """
    INSERT INTO Invoice (
        booker, dsr, customer_id, total, created_at
    ) VALUES (%s, %s, %s, %s, %s);
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            query,
            (
                data["booker"],
                data["dsr"],
                data["customer_id"],
                data["total"],
                data["date"],
            ),
        )
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        return f"Error adding Invoice: {str(e)}"


def list_invoices(sort_by="created_at", sort_order="ASC"):
    # Validate sort_by and sort_order to prevent SQL injection
    valid_sort_by = ["invoice_id", "booker_name", "delivery_man", "dsr", "customer_name", "total", "paid", "revision", "delivery_status", "payment_status", "notes", "created_at", "age"]
    valid_sort_order = ["ASC", "DESC"]

    if sort_by not in valid_sort_by:
        sort_by = "created_at"
    if sort_order not in valid_sort_order:
        sort_order = "ASC"

    query = f"""
    SELECT 
        i.invoice_id,
        e1.name AS booker_name,
        e2.name AS delivery_man, -- Updated alias to reflect nulls properly
        i.dsr,
        c.business_name AS customer_name,
        i.total,
        i.paid,
        i.revision,
        i.delivery_status,
        i.payment_status,
        i.notes,
        DATE(i.created_at) AS created_at,
        DATEDIFF(CURDATE(), i.created_at) AS age
    FROM Invoice i
    JOIN Employee e1 ON i.booker = e1.employee_id
    LEFT JOIN Employee e2 ON i.delivery_man = e2.employee_id
    JOIN Customers c ON i.customer_id = c.customer_id
    ORDER BY {sort_by} {sort_order};
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        return data
    except Exception as e:
        print(f"Error fetching invoices: {e}")
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
    delete_query = "DELETE FROM DispatchInvoice WHERE invoice_id = %s"
    try:
        cur = mysql.connection.cursor()
        cur.execute(delete_query, (invoice_id,))
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
        e2.name AS delivery_man_name, -- Updated alias to handle NULL values properly
        i.dsr,
        c.business_name AS customer_name,
        c.address AS customer_address, -- Updated alias for consistency
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
    LEFT JOIN Employee e2 ON i.delivery_man = e2.employee_id -- Use LEFT JOIN to handle NULL values
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


def edit_invoices(invoice_data):
    try:
        query = """
            UPDATE Invoice
            SET 
                paid = %s,
                revision = %s,
                notes = %s,
                delivery_status = %s
            WHERE invoice_id = %s
        """
        cur = mysql.connection.cursor()
        
        for invoice in invoice_data:
            paid = invoice.get('paid', 0)
            revision = invoice.get('revision', 0)
            notes = invoice.get('notes', '')
            delivery_status = invoice.get('delivery_status', 'Processed')
            invoice_id = invoice['invoice_id']
            
            cur.execute(query, (paid, revision, notes, delivery_status, invoice_id))

        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        return f"Error updating Invoice: {str(e)}"
