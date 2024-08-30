from flask import Blueprint, render_template, redirect, flash, url_for, request, jsonify
from flask_login import login_required, current_user


from Scripts.encryptions import password_is_valid
from Scripts.Database.users import list_users, finduser, add_user, edit_user, delete_user


user_bp = Blueprint("user", __name__)


@user_bp.route("/")
@login_required
def homee():
    data = list_users()
    return render_template("Users/list.html", current=current_user, data=data)


@user_bp.route("/<value>")
@login_required
def singleuser(value):
    val = int(value)
    user = finduser(False, val)
    print(user)
    return render_template("Users/view.html", current=current_user, data=user)


@user_bp.route("/add", methods=["GET", "POST"])
@login_required
def adduser():
    if request.method == "POST":
        data = request.form
        mandatory_fields = ["name", "last_name", "username", "password", "role", "status", "designation"]
        if all(field in data for field in mandatory_fields):
            password_valid, message = password_is_valid(data["password"])
            if not password_valid:
                flash(message, category="error")
                return redirect(url_for('user.adduser'))
            user_data = {
                "name": data.get("name"),
                "last_name": data.get("last_name"),
                "username": data.get("username"),
                "password": data.get("password"),
                "role": data.get("role"),
                "status": data.get("status"),
                "designation": data.get("designation"),
            }
            res = add_user(user_data)
            if res:
                mess = "User Added Successfully"
                flash(mess, category="success")
                return redirect(url_for('user.homee'))
            else:
                flash(res, category="error")
                return redirect(url_for('user.adduser'))
        else:
            missing_fields = [field for field in mandatory_fields if field not in data]
            mess = f"Missing required fields: {', '.join(missing_fields)}"
            flash(mess, category="error")
            return redirect(url_for('user.adduser'))
    else:
        return render_template("Users/add.html", current=current_user)


# ------------------ Edit-User Data ------------------ #
@user_bp.route("/edit/<value>", methods=["GET", "POST"])
@login_required
def editusers(value):
    if request.method == "POST":
        data = request.form
        mandatory_fields = ["name", "last_name", "username", "password", "role", "status", "designation"]
        if all(field in data for field in mandatory_fields):
            password_valid, message = password_is_valid(data["password"])
            if not password_valid:
                flash(message, category="error")
                return redirect(url_for('user.editusers', value=value))
            user_data = {
                "user_id": value,
                "name": data.get("name"),
                "last_name": data.get("last_name"),
                "password": data.get("password"),
                "role": data.get("role"),
                "status": data.get("status"),
                "designation": data.get("designation"),
            }
            res = edit_user(user_data)
            if res:
                mess = "User Edit Successfully"
                flash(mess, category="success")
                return redirect(url_for('user.singleuser', value=value))
            else:
                flash(res, category="error")
                return redirect(url_for('user.editusers', value=value))
        else:
            missing_fields = [field for field in mandatory_fields if field not in data]
            mess = f"Missing required fields: {', '.join(missing_fields)}"
            flash(mess, category="error")
            return redirect(url_for('user.editusers', value=value))
    else:
        val = int(value)
        user = finduser(False, val)
        return render_template("Users/edit.html", current=current_user, data=user)


# ------------------ Delete-User ------------------ #
@user_bp.route("/delete/<value>", methods=["GET"])
@login_required
def deleteuser(value):
    res = delete_user(value)
    if res == True:
        mess = "User Deleted Successfully"
        flash(mess, category="success")
        return redirect(url_for('user.homee'))
    else:
        flash(res, category="error")
        return redirect(url_for('user.homee'))
