from Scripts.extensions import mysql


def add_employee(data):
    query = """
    INSERT INTO Employee (
        customer_id, employee_amount, payment_status, delivery_status, delivery_id, notes, created_by
    ) VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            query,
            (
                data["customer_id"],
                data["employee_amount"],
                data["payment_status"],
                data["delivery_status"],
                data["delivery_id"],
                data["notes"],
                data["created_by"],
            ),
        )
        mysql.connection.commit()
        cur.close()
        return "employee Added Successfully", 200
    except Exception as e:
        return f"Error adding employee: {str(e)}", 400


def list_employees():
    query = "SELECT * FROM Employee"
    try:
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        return data
    except Exception as e:
        return f"Error listing employees: {str(e)}"


def edit_employee(data):
    query = """
    UPDATE Employee SET employee_amount = %s, payment_status = %s, 
    delivery_status = %s, delivery_id = %s, notes = %s, updated_at = CURRENT_TIMESTAMP 
    WHERE employee_id = %s
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            query,
            (
                data["employee_amount"],
                data["payment_status"],
                data["delivery_status"],
                data["delivery_id"],
                data["notes"],
                data["employee_id"],
            ),
        )
        affected_rows = cur.rowcount
        mysql.connection.commit()
        cur.close()
        return (
            "employee Edited Successfully",
            200 if affected_rows > 0 else "No matching record found for editing",
            404,
        )
    except Exception as e:
        return f"Error editing employee: {str(e)}", 400


def delete_employee(employee_id):
    query = "DELETE FROM Employee WHERE employee_id = %s"
    try:
        cur = mysql.connection.cursor()
        cur.execute(query, (employee_id,))
        affected_rows = cur.rowcount
        mysql.connection.commit()
        cur.close()
        return (
            "Employee Deleted Successfully",
            200 if affected_rows > 0 else "No matching record found for deletion",
            404,
        )
    except Exception as e:
        return f"Error deleting Employee: {str(e)}", 400
