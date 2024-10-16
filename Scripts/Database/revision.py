from Scripts.extensions import mysql


def list_revision():
    revision_query = """
        SELECT r.*, rs.reason 
        FROM Revision r
        JOIN reasons rs ON r.revision_reason = rs.reason_id;
    """
    
    try:
        cur = mysql.connection.cursor()
        cur.execute(revision_query)
        data = cur.fetchall()

        cur.close()
        return data
    except Exception as e:
        return False

    

def list_reason():
    query = "SELECT * FROM Reasons"

    try:
        cur = mysql.connection.cursor()
        cur.execute(query,)
        data = cur.fetchall()

        cur.close()
        return data
    except Exception as e:
        return False


def add_reason(reason):
    query = "INSERT INTO Reasons (reason) VALUES (%s)"

    try:
        cur = mysql.connection.cursor()
        cur.execute(query, (reason,))
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        return False


def edit_reason(reason_id, reason):
    query = "UPDATE Reasons SET reason = %s WHERE reason_id = %s"

    try:
        cur = mysql.connection.cursor()
        cur.execute(query, (reason, reason_id))
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        return False


def delete_reason(reason_id):
    query = "DELETE FROM Reasons WHERE reason_id = %s"

    try:
        cur = mysql.connection.cursor()
        cur.execute(query, (reason_id,))
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        return False
    

def add_revision(invoice_ids, revisions, reasons):
    query = """
        INSERT INTO Revision (invoice_id, revision, revision_reason)
        VALUES (%s, %s, %s)
    """

    try:
        cur = mysql.connection.cursor()
        for invoice_id, revision, reason in zip(invoice_ids, revisions, reasons):
            cur.execute(query, (invoice_id, revision, reason))

        mysql.connection.commit()  # Commit the changes
        cur.close()  # Close the cursor
        return True
    except Exception as e:
        print(f"Error adding revision: {e}")
        return False
