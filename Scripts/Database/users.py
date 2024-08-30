from Scripts.extensions import mysql
import bcrypt


def add_user(data):
    name = data["name"]
    lastname = data["last_name"]
    username = data["username"]
    _ = data["password"]
    role = data["role"]
    status = data["status"]
    desg = data["designation"]
    hashed = bcrypt.hashpw(_.encode('utf-8'), bcrypt.gensalt())
    
    query = """
    INSERT INTO Users (
        name, last_name, username, password, role, status, designation
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s
            );
    """
    try:

        cur = mysql.connection.cursor()
        cur.execute(query, (name, lastname, username, hashed, role, status, desg))
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        return "User Already Exists"


def finduser(username, user_id):
    if username:
        query = "SELECT * FROM Users WHERE username = '{value}'".format(value=username)
    if user_id:
        query = "SELECT * FROM Users WHERE id = '{value}'".format(value=user_id)
    try:
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        if data is None:
            return None
        else:
            return data
    except Exception as e:
        return None


def list_users():
    query = "SELECT * FROM Users"
    try:
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        return data
    except Exception as e:
        return "Table doesn't Exist"


def delete_user(value):
    try:
        cur = mysql.connection.cursor()

        # Check the number of users in the table
        cur.execute("SELECT COUNT(*) AS counts FROM Users")
        user_count = cur.fetchone()["counts"]

        if user_count > 1:
            query = "DELETE FROM Users WHERE id = %s"
            cur.execute(query, (value,))
            affected_rows = cur.rowcount  
            mysql.connection.commit()
            cur.close()

            if affected_rows > 0:
                return True
            else:
                return "No matching record found for deletion"
        else:
            cur.close()
            return "Cannot delete user. At least one user must remain."
    except Exception as e:
        return f"Error occurred: {str(e)}"


def edit_user(value):
    user_id = value["user_id"]
    name = value["name"]
    last_name = value["last_name"]
    password = value["password"]
    role = value["role"]
    status = value["status"]
    designation = value["designation"]

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Update query to include all fields
    query = """
    UPDATE Users 
    SET name = %s, last_name = %s, password = %s, role = %s, status = %s, designation = %s 
    WHERE id = %s
    """

    try:
        cur = mysql.connection.cursor()
        cur.execute(query, (name, last_name, hashed_password, role, status, designation, user_id))
        affected_rows = cur.rowcount
        mysql.connection.commit()
        cur.close()

        if affected_rows > 0:
            return True
        else:
            return "No matching record found for editing"
    except Exception as e:
        return "Error editing User: {}".format(str(e))

