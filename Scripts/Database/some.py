from flask_login import UserMixin
from Scripts.extensions import mysql


class User(UserMixin):
    def __init__(self, id, name, username, role, status, designation):
        self.id = id
        self.name = name
        self.username = username
        self.role = role
        self.status = status
        self.designation = designation

    @classmethod
    def get(cls, user_id):
        # This method should query the database and return a User object
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            return cls(
                id=user["id"],
                name=user["name"],
                username=user["username"],
                role=user["role"],
                status=user["status"],
                designation=user["designation"],
            )
        return None

    @classmethod
    def get_by_username(cls, username):
        # This method should query the database and return a User object
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            return cls(
                id=user["id"],
                name=user["name"],
                username=user["username"],
                role=user["role"],
                status=user["status"],
                designation=user["designation"],
            )
        return None
