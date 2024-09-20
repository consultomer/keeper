from flask import jsonify, render_template, Blueprint
from flask_login import login_required, current_user

from Scripts.Database.db import (
    find_total,
    c_user,
)


# from flask_cors import CORS


route_bp = Blueprint("routes", __name__)


# ------------------ Home ------------------ #
@route_bp.route("/")
@login_required
def home():
    data = find_total()
    return render_template("dashboard.html", current=current_user, total=data)


# ------------------ Create User ------------------ #
@route_bp.route("/usercr", methods=["GET"])
def ct():
    res = c_user
    return jsonify({"data": res})

