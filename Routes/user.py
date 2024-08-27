from flask import Blueprint, render_template, request, jsonify
import jwt, random

from Scripts.encryptions import password_is_valid
# from Scripts.Database.users import edit_user, delete_user


user_bp = Blueprint('user', __name__)

@user_bp.route("/")
def useer():
    data = [
        {
            "id": 1,
            "name": random.choice(["Omer", "Ali", "Sara", "Aisha", "Ahmed"]),
            "last_name": random.choice(["Rehman", "Khan", "Butt", "Hassan", "Shah"]),
            "username": f"user{random.randint(1000, 9999)}",
            "role": random.choice(["admin", "user", "guest"]),
            "status": random.choice(["active", "inactive"]),
        },
        {
            "id": 2,
            "name": random.choice(["Omer", "Ali", "Sara", "Aisha", "Ahmed"]),
            "last_name": random.choice(["Rehman", "Khan", "Butt", "Hassan", "Shah"]),
            "username": f"user{random.randint(1000, 9999)}",
            "role": random.choice(["admin", "user", "guest"]),
            "status": random.choice(["active", "inactive"]),
        },
        {
            "id": 3,
            "name": random.choice(["Omer", "Ali", "Sara", "Aisha", "Ahmed"]),
            "last_name": random.choice(["Rehman", "Khan", "Butt", "Hassan", "Shah"]),
            "username": f"user{random.randint(1000, 9999)}",
            "role": random.choice(["admin", "user", "guest"]),
            "status": random.choice(["active", "inactive"]),
        },
    ]
    
    return render_template("users.html", data=data)


@user_bp.route("/<value>")
def singleuser(value):
    val = int(value)
    data = [
        {
            "id": 1,
            "name": random.choice(["Omer", "Ali", "Sara", "Aisha", "Ahmed"]),
            "last_name": random.choice(["Rehman", "Khan", "Butt", "Hassan", "Shah"]),
            "username": f"user{random.randint(1000, 9999)}",
            "role": random.choice(["admin", "user", "guest"]),
            "status": random.choice(["active", "inactive"]),
        },
        {
            "id": 2,
            "name": random.choice(["Omer", "Ali", "Sara", "Aisha", "Ahmed"]),
            "last_name": random.choice(["Rehman", "Khan", "Butt", "Hassan", "Shah"]),
            "username": f"user{random.randint(1000, 9999)}",
            "role": random.choice(["admin", "user", "guest"]),
            "status": random.choice(["active", "inactive"]),
        },
        {
            "id": 3,
            "name": random.choice(["Omer", "Ali", "Sara", "Aisha", "Ahmed"]),
            "last_name": random.choice(["Rehman", "Khan", "Butt", "Hassan", "Shah"]),
            "username": f"user{random.randint(1000, 9999)}",
            "role": random.choice(["admin", "user", "guest"]),
            "status": random.choice(["active", "inactive"]),
        },
    ]
    user = next((item for item in data if item["id"] == val), None)

    if user:
        return user
    return render_template("users.html", data=data[val])


@user_bp.route("/add")
def formss():
    return render_template("new.html")


# ------------------ Edit-User Data ------------------ #
@user_bp.route("/edit", methods=["POST"])
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
