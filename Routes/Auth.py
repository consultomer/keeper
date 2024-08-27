from flask import request, jsonify, session, Blueprint, render_template
from datetime import datetime, timedelta
import jwt, bcrypt

# from Scripts.Database.users import finduser
from Scripts.encryptions import decrypt_ps, password_is_valid

auth_bp = Blueprint("auth", __name__)





# ------------------ Login ------------------ #
@auth_bp.route("/login", methods=["GET", "POST"])
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
                # token = jwt.encode(payload, app.secret_key, algorithm="HS256")
                return jsonify({"token": "token"}), 200
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
    else:
        return render_template("login.html")


# ------------------ Logout ------------------ #
@auth_bp.route("/logout", methods=["POST"])
def disconnect():
    if request.method == "POST":
        token = request.headers.get("Authorization").split()[1]

    try:
        # decoded_token = jwt.decode(token, app.secret_key, algorithms=["HS256"])
        # user_id = decoded_token["user_id"]
        session.pop("user_id", None)
        return jsonify({"Logout": "True"}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
