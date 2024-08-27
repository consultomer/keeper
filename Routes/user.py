from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
import jwt, random

from Scripts.encryptions import password_is_valid
from Scripts.Database.users import list_users, finduser,edit_user, delete_user


user_bp = Blueprint('user', __name__)

@user_bp.route("/")
@login_required
def useer():
    data = list_users()
    
    return render_template("users.html", data=data)


@user_bp.route("/<value>")
@login_required
def singleuser(value):
    val = int(value)
    user = finduser(False, val)
    print(user)
    return user
    return render_template("users.html", data=data[val])


@user_bp.route("/add")
@login_required
def formss():
    return render_template("adduser.html")


# ------------------ Edit-User Data ------------------ #
@user_bp.route("/edit", methods=["POST"])
@login_required
def editusers():
    if request.method == "POST":
        token = request.headers.get("Authorization").split()[1]

        try:
            # decoded_token = jwt.decode(token, app.secret_key, algorithms=["HS256"])
            # user_id = decoded_token["user_id"]
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
@user_bp.route("/delete/<value>")
@login_required
def deleteuser(value):
    token = request.headers.get("Authorization").split()[1]

    try:
        # decoded_token = jwt.decode(token, app.secret_key, algorithms=["HS256"])
        # user_id = decoded_token["user_id"]
        res = delete_user(value)
        return jsonify({"data": res}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
