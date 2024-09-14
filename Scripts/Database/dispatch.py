from Scripts.extensions import mysql


def add_dispatch(data, invoice_ids):
    try:
        delivery_man = data["delivery_man"]
        delivery_status = data["delivery_status"]
        payment_status = data["payment_status"]
        
        # Insert into Dispatch
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO Dispatch (delivery_man, delivery_status, payment_status)
            VALUES (%s, %s, %s)
        """, (delivery_man, delivery_status, payment_status))
        
        dispatch_id = cur.lastrowid  # Get the last inserted dispatch_id
        
        # Insert into DispatchInvoice
        for invoice_id in invoice_ids:
            cur.execute("""
                INSERT INTO DispatchInvoice (dispatch_id, invoice_id)
                VALUES (%s, %s)
            """, (dispatch_id, invoice_id))
        
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        return f"Error: {e}"


def list_dispatch(sort_by="created_at", sort_order="ASC"):
    # Validate sort_by and sort_order to prevent SQL injection
    valid_sort_by = [
        "dispatch_id", "delivery_man", "invoice", "total", 
        "paid", "delivery_status", "payment_status", 
        "notes", "created_at", "updated_at"
    ]
    valid_sort_order = ["ASC", "DESC"]

    if sort_by not in valid_sort_by:
        sort_by = "created_at"
    if sort_order not in valid_sort_order:
        sort_order = "ASC"
    
    query = f"""
    SELECT 
        d.dispatch_id,
        d.delivery_man,
        GROUP_CONCAT(i.invoice_id ORDER BY i.invoice_id SEPARATOR ', ') AS invoice,
        SUM(i.total) AS total,
        SUM(i.paid) AS paid,
        d.delivery_status,
        d.payment_status,
        d.notes,
        d.created_at,
        d.updated_at
    FROM 
        Dispatch d
    JOIN 
        DispatchInvoice dc ON d.dispatch_id = dc.dispatch_id
    JOIN 
        Invoice i ON dc.invoice_id = i.invoice_id
    GROUP BY 
        d.dispatch_id
    ORDER BY 
        {sort_by} {sort_order};
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        return data
    except Exception as e:
        print(f"Error fetching dispatches: {e}")
        return False


def view_dispatch(dispatch_id):
    dispatch_query = """
        SELECT 
            d.dispatch_id,
            d.delivery_man,
            d.delivery_status AS deli_status,
            d.payment_status AS pay_status,
            SUM(i.total) - SUM(i.paid) AS remaining,
            d.created_at AS date
        FROM 
            Dispatch d
        JOIN 
            DispatchInvoice di ON d.dispatch_id = di.dispatch_id
        JOIN 
            Invoice i ON di.invoice_id = i.invoice_id
        WHERE 
            d.dispatch_id = %s
        GROUP BY 
            d.dispatch_id;
        """        
        # Query to fetch related invoices
    invoices_query = """
        SELECT 
            i.invoice_id,
            c.business_name AS customer_name,
            i.total,
            i.paid,
            (i.total - i.paid) AS remaining
        FROM 
            Invoice i
        JOIN 
            DispatchInvoice di ON i.invoice_id = di.invoice_id
        JOIN 
            Customers c ON i.customer_id = c.customer_id
        WHERE 
            di.dispatch_id = %s;
        """

    try:
        cur = mysql.connection.cursor()
        cur.execute(dispatch_query, (dispatch_id,))
        dispatch_data = cur.fetchone()
        cur.execute(invoices_query, (dispatch_id,))
        invoices_data = cur.fetchall()
        cur.close()
        return dispatch_data, invoices_data
    except Exception as e:
        print(f"Error fetching dispatches: {e}")
        return False
    

def delete_dispatch(dispatch_id):
    delete_dispatch_invoices_query = """
    DELETE FROM DispatchInvoice WHERE dispatch_id = %s;
    """
    delete_dispatch_query = """
    DELETE FROM Dispatch WHERE dispatch_id = %s;
    """
    
    try:
        cur = mysql.connection.cursor()
        
        # Delete related records from DispatchInvoice first
        cur.execute(delete_dispatch_invoices_query, (dispatch_id,))
        
        # Then delete the dispatch record
        cur.execute(delete_dispatch_query, (dispatch_id,))
        
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        print(f"Error deleting dispatch: {e}")
        return False
