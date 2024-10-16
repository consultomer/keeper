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


def list_invoices(sort_by="created_at", sort_order="ASC", status="Un-delivered"):
    # Validate sort_by and sort_order to prevent SQL injection
    valid_sort_by = [
        "invoice_id",
        "booker_name",
        "delivery_man",
        "dsr",
        "customer_name",
        "total",
        "paid",
        "revision",
        "delivery_status",
        "payment_status",
        "notes",
        "created_at",
        "age",
    ]
    valid_sort_order = ["ASC", "DESC"]

    # Ensure the sort_by and sort_order are valid, else use defaults
    if sort_by not in valid_sort_by:
        sort_by = "created_at"
    if sort_order not in valid_sort_order:
        sort_order = "ASC"

    # Base query to fetch invoices
    query = """
    SELECT 
        i.invoice_id,
        e1.name AS booker_name,
        e2.name AS delivery_man,
        i.dsr,
        c.business_name AS customer_name,
        i.total,
        i.paid,
        i.delivery_status,
        i.payment_status,
        DATE(i.created_at) AS created_at,
        DATEDIFF(CURDATE(), i.created_at) AS age
    FROM Invoice i
    JOIN Employee e1 ON i.booker = e1.employee_id
    LEFT JOIN Employee e2 ON i.delivery_man = e2.employee_id
    JOIN Customers c ON i.customer_id = c.customer_id
    """

    # Apply status filter
    if status:
        query += " WHERE i.delivery_status = 'Delivered'"
    else:
        query += " WHERE i.delivery_status != 'Delivered'"
    # If no valid status is provided, fetch all invoices

    # Add sorting clause
    query += f" ORDER BY {sort_by} {sort_order}"

    try:
        cur = mysql.connection.cursor()  # Use dictionary=True for easier access
        cur.execute(query)
        invoices = cur.fetchall()

        # Fetch revisions for each invoice
        for invoice in invoices:
            invoice_id = invoice['invoice_id']
            
            # Query to get the sum of revisions for a specific invoice
            revision_sum_query = """
                SELECT SUM(revision) AS total_revision 
                FROM Revision 
                WHERE invoice_id = %s
            """
            
            cur.execute(revision_sum_query, (invoice_id,))
            total_revision = cur.fetchone()['total_revision'] or 0  # Handle NULL case
            
            # Attach the total sum of revisions to the invoice
            invoice['revision'] = total_revision
            invoice['current_value'] = invoice['total'] - invoice['paid'] + total_revision


        cur.close()
        return invoices
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
        SET booker = %s, delivery_man = %s, dsr = %s, customer_id = %s, total = %s, paid = %s, company = %s, delivery_status = %s, payment_status = %s
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
                data["delivery_status"],
                data["payment_status"],
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
    # Query to fetch invoice details
    query = """
    SELECT 
        i.invoice_id,
        e1.name AS booker_name,
        e2.name AS delivery_man_name, -- Use LEFT JOIN to handle NULL values
        i.dsr,
        c.business_name AS customer_name,
        c.address AS customer_address,
        c.phone AS customer_phone,
        i.total,
        i.paid,
        i.company,
        i.delivery_status,
        i.payment_status,
        DATE(i.created_at) AS created_at,
        DATEDIFF(CURDATE(), i.created_at) AS age
    FROM Invoice i
    JOIN Employee e1 ON i.booker = e1.employee_id
    LEFT JOIN Employee e2 ON i.delivery_man = e2.employee_id -- Use LEFT JOIN for NULL delivery_man
    JOIN Customers c ON i.customer_id = c.customer_id
    WHERE i.invoice_id = %s;
    """
    
    # Query to fetch revisions for the invoice
    revision_query = """
        SELECT r.revision, rs.reason 
        FROM Revision r
        JOIN reasons rs ON r.revision_reason = rs.reason_id
    WHERE r.invoice_id = %s;
    """
    
    try:
        cur = mysql.connection.cursor()
        
        # Execute the invoice query
        cur.execute(query, (value,))
        data = cur.fetchall()
        
        if not data:  # Check if no data is returned
            return {"error": "Invoice not found."}
        
        # Execute the revision query
        cur.execute(revision_query, (value,))
        revisions = cur.fetchall()
        
        cur.close()
        
        # Add revisions to the first invoice result
        data[0]['revisions'] = revisions  # Add revisions field
        
        return data[0]  # Return the invoice details with revisions
    
    except Exception as e:
        # Handle exceptions and print error for debugging
        print(f"Error fetching invoice: {e}")
        return {"error": "An error occurred while fetching the invoice."}



def edit_invoices(invoice_data):
    try:
        query = """
            UPDATE Invoice
            SET 
                paid = %s,
                delivery_status = %s
            WHERE invoice_id = %s
        """
        cur = mysql.connection.cursor()

        for invoice in invoice_data:
            paid = invoice.get("paid", 0)
            revisions = invoice.get("revision", [])
            print(revisions)
            delivery_status = invoice.get("delivery", "Processed")
            invoice_id = invoice["invoice_id"]

            cur.execute(query, (paid, delivery_status, invoice_id))
            insert_revision_query = """
                INSERT INTO Revision (invoice_id, revision, revision_reason)
                VALUES (%s, %s, %s)
            """
            for rev in revisions:
                print(rev)
                cur.execute(insert_revision_query, (invoice_id, rev["revision"], rev["revision_reason"]))


        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        return f"Error updating Invoice: {str(e)}"
