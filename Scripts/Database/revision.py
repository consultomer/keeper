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