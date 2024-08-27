from extensions import mysql
import bcrypt


def add_user(data):
    name = data["name"]
    lastname = data["lastname"]
    username = data["username"]
    _ = data["password"]
    role = data["role"]
    hashed = bcrypt.hashpw(_, bcrypt.gensalt())
    query = """
    INSERT INTO Users (
        name, last_name, username, password, role, status, designation
        ) VALUES (
            %s, %s, %s, %s, %s, 'is_active', 'none'
            );
    """
    try:

        cur = mysql.connection.cursor()
        cur.execute(query, (name, lastname, username, hashed, role))
        mysql.connection.commit()
        cur.close()
        return "User Added Successfully", 200
    except Exception as e:
        return "User Already Exists", 400


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
                return "User Deleted Successfully", 200
            else:
                return "No matching record found for deletion", 404
        else:
            cur.close()
            return "Cannot delete user. At least one user must remain.", 403
    except Exception as e:
        return f"Error occurred: {str(e)}", 403


def edit_user(value):
    user_id = value["user_id"]
    _ = value["password"]
    hashed = bcrypt.hashpw(_, bcrypt.gensalt())

    query = "UPDATE Users SET password = %s WHERE id = %s"
    try:
        cur = mysql.connection.cursor()
        cur.execute(query, (hashed, user_id))
        affected_rows = cur.rowcount
        mysql.connection.commit()
        cur.close()

        if affected_rows > 0:
            return "User Edited Successfully", 200
        else:
            return "No matching record found for editing", 404
    except Exception as e:
        return "Error editing User: {}".format(str(e)), 401
