from flask_login import UserMixin
from extensions import mysql

class User(UserMixin):
    def __init__(self, id, username, password, role, status, desgination):
        self.id = id
        self.username = username
        self.password = password
        self.role = role
        self.status = status
        self.desgination = desgination

    @classmethod
    def get(cls, user_id):
        # This method should query the database and return a User object
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            return cls(
                id=user['id'],
                username=user['username'],
                password=user['password'],
                role=user['role'],
                status=user['status'],
                desgination=user['desgination']
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
                id=user['id'],
                username=user['username'],
                password=user['password'],
                role=user['role'],
                status=user['status'],
                desgination=user['desgination']
            )
        return None
