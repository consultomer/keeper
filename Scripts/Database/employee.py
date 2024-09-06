from Scripts.extensions import mysql


def add_employee(data):
    name = data["name"]
    role = data["role"]
    phone_number = data["phone_number"]
    whatsapp_number = data["whatsapp_number"]
    address = data["address"]
    company = data["company"]
    query = """
    INSERT INTO Employee (
        name, role, phone_number, whatsapp_number, address, company
    ) VALUES (%s, %s, %s, %s, %s, %s);
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            query,
            (
                name,
                role,
                phone_number,
                whatsapp_number,
                address,
                company,
            ),
        )
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        return f"Error adding employee: {str(e)}"


def find_employee(int):
    query = "SELECT * FROM Employee WHERE employee_id = %s"
    try:
        cur = mysql.connection.cursor()
        cur.execute(query, (int,))
        data = cur.fetchall()
        cur.close()
        return data if data else None
    except Exception as e:
        return f"Error finding Customer: {str(e)}"


def list_employees(page, per_page):
    offset = (page - 1) * per_page
    query = "SELECT * FROM Employee LIMIT %s OFFSET %s"
    count_query = "SELECT COUNT(*) AS total FROM Employee"

    try:
        cur = mysql.connection.cursor()
        cur.execute(query, (per_page, offset))
        data = cur.fetchall()

        cur.execute(count_query)
        total_count = cur.fetchone()["total"]

        cur.close()
        return data, total_count
    except Exception as e:
        return False


def edit_employee(data):
    query = """
    UPDATE Employee SET name = %s, role = %s, 
    phone_number = %s, whatsapp_number = %s, address = %s, company = %s  
    WHERE employee_id = %s
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            query,
            (
                data["name"],
                data["role"],
                data["phone_number"],
                data["whatsapp_number"],
                data["address"],
                data["company"],
                data["employee_id"],
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
        return f"Error editing Employee: {str(e)}"


def delete_employee(employee_id):
    query = "DELETE FROM Employee WHERE employee_id = %s"
    try:
        cur = mysql.connection.cursor()
        cur.execute(query, (employee_id,))
        affected_rows = cur.rowcount
        mysql.connection.commit()
        cur.close()
        if affected_rows > 0:
            return True
        else:
            return "No matching record found for deletion"
    except Exception as e:
        return f"Error deleting Employee: {str(e)}"


def employee():
    query = """
    SELECT employee_id, role, name
    FROM Employee;
    """
    try:
        # Assuming `mysql` is your connection object, replace this with your actual connection method if different
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
