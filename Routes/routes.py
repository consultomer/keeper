from flask import jsonify, render_template, Blueprint
from flask_login import login_required, current_user

from Scripts.Database.db import (
    find_total,
    initialize_database,
)


# from flask_cors import CORS


route_bp = Blueprint("routes", __name__)


# ------------------ Home ------------------ #
@route_bp.route("/")
@login_required
def home():
    data = find_total()
    return render_template("dashboard.html", current=current_user, total=data)


# ------------------ Initialize_Database ------------------ #
@route_bp.route("/initialize_database", methods=["GET"])
def ct():
    res = initialize_database()
    return jsonify({"data": res})
