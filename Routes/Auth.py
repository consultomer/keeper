from flask import request, Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user, UserMixin
from extensions import login_manager
from Scripts.Database.some import User
import bcrypt

from Scripts.Database.users import finduser
from Scripts.encryptions import password_is_valid


auth_bp = Blueprint("auth", __name__)


@login_manager.user_loader
def load_user(id):
    data = finduser(username=None, user_id=id)
    user_data = data[0]
    return user_data

# ------------------ Login ------------------ #
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not username or not password:
            mess = "username and password are required"
            return render_template("login.html", message = mess)

        data = User.get_by_username(username)
        if data:
            print(data)
            user_data = data[0]
            _ = password.encode("utf-8")
            hashed = user_data.password.encode("utf-8")
            if bcrypt.checkpw(_, hashed):
                # login_user(User(id=user_data['id'], name=user_data["name"], username=user_data['username'], password=user_data['password']), remember=True)
                login_user(data, remember=True)
                return redirect(url_for('routes.home'))
            else:
                mess = "Wrong Credentials"
                return render_template("login.html", message=mess)
        else:
            mess = "User not Available"
            return render_template("login.html", message=mess)
    else:
        return render_template("login.html", user=current_user)

@auth_bp.route('/test_user')
@login_required
def test_user():
    user = User(id=1, name="Omer", username="omer123", password="password")
             # Should return the `id` of the user

    # Return a response for verification
    return f"is_authenticated: {user.is_authenticated}, is_active: {user.is_active}, is_anonymous: {user.is_anonymous}, get_id: {user.get_id}"

# ------------------ Logout ------------------ #
@auth_bp.route("/logout", methods=["GET", "POST"])
def disconnect():

    return f"Hello, {current_user}"
