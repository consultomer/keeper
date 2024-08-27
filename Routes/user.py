from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_required
import jwt, random

from Scripts.encryptions import password_is_valid
from Scripts.Database.users import list_users, finduser, edit_user, delete_user


user_bp = Blueprint("user", __name__)


@user_bp.route("/")
@login_required
def homee():
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
        data = request.json
        mandatory_fields = ["user_id", "password"]
        if all(field in data for field in mandatory_fields):
            password_valid, message = password_is_valid(data["password"])
            if not password_valid:
                return jsonify({"error": message}), 400

            res = edit_user(data)
            return jsonify({"data": res})
        else:
            missing_fields = [field for field in mandatory_fields if field not in data]
            return (
                jsonify(
                    {"error": f"Missing required fields: {', '.join(missing_fields)}"}
                ),
                400,
            )


# ------------------ Delete-User ------------------ #
@user_bp.route("/delete/<value>")
@login_required
def deleteuser(value):
    res = delete_user(value)
    flash(res, category="success")
    return redirect(url_for("user.homee"))
