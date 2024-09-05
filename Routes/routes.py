from flask import jsonify, render_template, Blueprint
from flask_login import login_required, current_user

from Scripts.Database.db import (
    create_customer_table,
    create_employee_table,
    create_invoice_table,
    create_users_table,
    find_total
)


# from flask_cors import CORS


route_bp = Blueprint("routes", __name__)


# ------------------ Home ------------------ #
@route_bp.route("/")
@login_required
def home():
    data = find_total()
    return render_template("dashboard.html", current=current_user, total=data)


# ------------------ Random ------------------ #
@route_bp.route("/createtable", methods=["GET"])
def ct():
    # res = create_users_table()
    # res1 = create_customer_table()
    # res2 = create_employee_table()
    res3 = create_invoice_table()
    return jsonify({"data": res3})


#     res2 = create_employee_table()
#     res4 = create_payment_table()
#     res5 = create_credit_table()
#     res6 = create_deliverylog_table()
#     res7 = create_invoice_adj_table()

#     return jsonify(
#         {
#             "message": [
#                 res,
#                 res1,
#                 res3,
#                 res4,
#                 res5,
#                 res6,
#                 res7,
#                 res8,
#                 res9
#             ]
#         }
#     )
