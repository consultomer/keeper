from Scripts.extensions import mysql





def add_dispatch(data, invoice_ids):
    try:
        delivery_man = data["delivery_man"]
        total = data["total_amount"]
        paid = data["paid"]
        delivery_status = data["delivery_status"]
        payment_status = data["payment_status"]
        
        # Insert into Dispatch
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO Dispatch (delivery_man, total, paid, delivery_status, payment_status)
            VALUES (%s, %s, %s, %s, %s)
        """, (delivery_man, total, paid, delivery_status, payment_status))
        
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
