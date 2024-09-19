from Scripts.extensions import mysql


def add_dispatch(data, invoice_ids):
    try:
        print(f"data: {data}, type: {type(data)}")
        print(f"invoice_ids: {invoice_ids}, type: {type(invoice_ids)}")
        delivery_man = int(data)
        
        # Insert into Dispatch
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO Dispatch (delivery_man)
            VALUES (%s)
        """, (delivery_man,))
        
        dispatch_id = cur.lastrowid  # Get the last inserted dispatch_id
        
        # Query for inserting into Dispatch_Invoice
        query = """
            INSERT INTO DispatchInvoice (dispatch_id, invoice_id)
            VALUES (%s, %s)
        """
        
        # Query for updating Invoice table
        query2 = """
        UPDATE Invoice
        SET 
            delivery_man = %s,
            delivery_status = 'Processing',
            company = (SELECT company FROM Employee WHERE employee_id = %s)
        WHERE invoice_id = %s;
        """
        
        for invoice_id in invoice_ids:
            cur.execute(query, (dispatch_id, invoice_id))
            cur.execute(query2, (delivery_man, delivery_man, invoice_id))
        
        # Commit the changes
        mysql.connection.commit()
        cur.close()
        return True

    except Exception as e:
        return f"Error: {e}"



def list_dispatches(sort_by="dispatch_date", sort_order="ASC"):
    # Validate sort_by and sort_order to prevent SQL injection
    valid_sort_by = ["dispatch_id", "delivery_man", "dispatch_date"]
    valid_sort_order = ["ASC", "DESC"]

    if sort_by not in valid_sort_by:
        sort_by = "dispatch_date"
    if sort_order not in valid_sort_order:
        sort_order = "ASC"

    query = f"""
    SELECT 
        d.dispatch_id,
        e.name AS delivery_man,
        DATE(d.dispatch_date) AS dispatch_date,
        JSON_ARRAYAGG(
            JSON_OBJECT(
                'invoice_id', i.invoice_id,
                'total', i.total,
                'paid', i.paid,
                'delivery_status', i.delivery_status,
                'payment_status', i.payment_status,
                'booker', b.name,
                'dsr', i.dsr,
                'customer_name', c.business_name,
                'company', i.company,
                'revision', i.revision,
                'age', DATEDIFF(CURRENT_DATE, i.created_at)
            )
        ) AS invoices
    FROM Dispatch d
    JOIN Employee e ON d.delivery_man = e.employee_id
    JOIN DispatchInvoice di ON d.dispatch_id = di.dispatch_id
    JOIN Invoice i ON di.invoice_id = i.invoice_id
    JOIN Employee b ON i.booker = b.employee_id
    JOIN Customers c ON i.customer_id = c.customer_id
    GROUP BY d.dispatch_id, e.name, d.dispatch_date
    ORDER BY {sort_by} {sort_order};
    """

    try:
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        print(data)
        return data
    except Exception as e:
        print(f"Error fetching dispatches: {e}")
        return False


def view_dispatch(dispatch_id):
    dispatch_query = """
        SELECT 
            d.dispatch_id,
            e.name AS delivery_man,
            DATE(d.dispatch_date) AS dispatch_date,
            JSON_ARRAYAGG(
                JSON_OBJECT(
                    'invoice_id', i.invoice_id,
                    'total', i.total,
                    'paid', i.paid,
                    'delivery_status', i.delivery_status,
                    'payment_status', i.payment_status,
                    'booker', b.name,
                    'dsr', i.dsr,
                    'customer_name', c.business_name,
                    'notes', i.notes,
                    'revision', i.revision,
                    'age', DATEDIFF(CURRENT_DATE, i.created_at)
                )
            ) AS invoices
        FROM Dispatch d
        JOIN Employee e ON d.delivery_man = e.employee_id
        JOIN DispatchInvoice di ON d.dispatch_id = di.dispatch_id
        JOIN Invoice i ON di.invoice_id = i.invoice_id
        JOIN Employee b ON i.booker = b.employee_id
        JOIN Customers c ON i.customer_id = c.customer_id
        WHERE d.dispatch_id = %s
        GROUP BY d.dispatch_id, e.name, d.dispatch_date;
        """

    try:
        cur = mysql.connection.cursor()
        cur.execute(dispatch_query, (dispatch_id,))
        dispatch_data = cur.fetchone()
        cur.close()
        return dispatch_data
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
