
from flask import request, jsonify, session, Blueprint
from datetime import datetime, timedelta
import jwt, bcrypt


# from Scripts.Database.users import (
#     add_user,
#     finduser,
#     list_users,
#     delete_user,
#     edit_user,
# )
from Scripts.encryptions import decrypt_ps, password_is_valid

auth_bp = Blueprint("auth", __name__)

# ------------------ Registration -------------------#
@auth_bp.route("/add", methods=["POST"])
def register():
    if request.method == "POST":
        token = request.headers.get("Authorization").split()[1]

        try:
            decoded_token = jwt.decode(token, app.secret_key, algorithms=["HS256"])
            user_id = decoded_token["user_id"]
            data = request.json
            mandatory_fields = ["name", "lastname", "username", "password", "role"]
            if all(field in data for field in mandatory_fields):
                password_valid, message = password_is_valid(data["password"])
                if not password_valid:
                    return jsonify({"error": message}), 400

                result_message = add_user(data)

                return result_message
            else:
                missing_fields = [
                    field for field in mandatory_fields if field not in data
                ]
                return (
                    jsonify(
                        {
                            "error": f"Missing required fields: {', '.join(missing_fields)}"
                        }
                    ),
                    400,
                )

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401


# ------------------ Login ------------------ #
@auth_bp.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        username = request.json["email"]
        paword = request.json["password"]
        if not username or not paword:
            return jsonify({"message": "username and password are required"}), 400

        data = finduser(username, user_id=None)
        lcense_value = "False"
        if data:
            _ = decrypt_ps(paword)

            hashed = data[2].encode("utf-8")
            if bcrypt.checkpw(_, hashed):
                session["user_id"] = str(data[0])
                payload = {
                    "user_id": str(data[0]),
                    "exp": datetime.utcnow() + timedelta(minutes=600),
                }
                token = jwt.encode(payload, app.secret_key, algorithm="HS256")
                return jsonify({"token": token}), 200
            else:
                return (
                    jsonify({"message": "Wrong Password"}),
                    401,
                )
        else:
            return (
                jsonify({"message": "User Doesn't Exist"}),
                404,
            )


# ------------------ Logout ------------------ #
@auth_bp.route("/logout", methods=["POST"])
def disconnect():
    if request.method == "POST":
        token = request.headers.get("Authorization").split()[1]

    try:
        decoded_token = jwt.decode(token, app.secret_key, algorithms=["HS256"])
        user_id = decoded_token["user_id"]
        session.pop("user_id", None)
        return jsonify({"Logout": "True"}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401


# ------------------ List-Users Data ------------------ #
@auth_bp.route("/list")
def listusers():
    token = request.headers.get("Authorization").split()[1]

    try:
        decoded_token = jwt.decode(token, app.secret_key, algorithms=["HS256"])
        user_id = decoded_token["user_id"]
        res = list_users()
        return jsonify({"data": res}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401


# ------------------ Edit-User Data ------------------ #
@auth_bp.route("/edit", methods=["POST"])
def editusers():
    if request.method == "POST":
        token = request.headers.get("Authorization").split()[1]

        try:
            decoded_token = jwt.decode(token, app.secret_key, algorithms=["HS256"])
            user_id = decoded_token["user_id"]
            data = request.json
            mandatory_fields = ["user_id", "password"]
            if all(field in data for field in mandatory_fields):
                password_valid, message = password_is_valid(data["password"])
                if not password_valid:
                    return jsonify({"error": message}), 400

                res = edit_user(data)
                return jsonify({"data": res})
            else:
                missing_fields = [
                    field for field in mandatory_fields if field not in data
                ]
                return (
                    jsonify(
                        {
                            "error": f"Missing required fields: {', '.join(missing_fields)}"
                        }
                    ),
                    400,
                )
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401


# ------------------ Delete-User ------------------ #
@auth_bp.route("/delete/<object_id>")
def deleteuser(object_id):
    token = request.headers.get("Authorization").split()[1]

    try:
        decoded_token = jwt.decode(token, app.secret_key, algorithms=["HS256"])
        user_id = decoded_token["user_id"]
        res = delete_user(object_id)
        return jsonify({"data": res}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
