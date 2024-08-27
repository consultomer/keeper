from flask import request, Blueprint, render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user
from extensions import login_manager
from Scripts.Database.some import User
import bcrypt



auth_bp = Blueprint("auth", __name__)


@login_manager.user_loader
def load_user(id):
    data = User.get(id)
    return data


# ------------------ Login ------------------ #
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not username or not password:
            mess = "username and password are required"
            return render_template("login.html", message=mess)

        data = User.get_by_username(username)
        if data:
            _ = password.encode("utf-8")
            hashed = data.password.encode("utf-8")
            if bcrypt.checkpw(_, hashed):
                login_user(data, remember=True)
                return redirect(url_for("routes.home"))
            else:
                mess = "Wrong Credentials"
                return render_template("login.html", message=mess)
        else:
            mess = "User not Available"
            return render_template("login.html", message=mess)
    else:
        return render_template("login.html")


# ------------------ Logout ------------------ #
@auth_bp.route("/logout", methods=["GET"])
@login_required
def disconnect():
    logout_user()
    return redirect(url_for("auth.login"))
