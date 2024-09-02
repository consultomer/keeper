from flask import jsonify, render_template, Blueprint
from flask_login import login_required, current_user

from Scripts.Database.db import (
    create_credit_table,
    create_customer_table,
    create_deliverylog_table,
    create_employee_table,
    create_invoice_adj_table,
    create_invoice_table,
    create_orderbooker_table,
    create_payment_table,
    create_users_table,
)


# from flask_cors import CORS


route_bp = Blueprint("routes", __name__)


# ------------------ Home ------------------ #
@route_bp.route("/")
@login_required
def home():
    return render_template("base.html", current=current_user)


# ------------------ Random ------------------ #
@route_bp.route("/createtable", methods=["GET"])
def ct():
    # res = create_users_table()
    # res1 = create_customer_table()
    res2 = create_employee_table()
    return jsonify({"data": res2})


#     res2 = create_employee_table()
#     res3 = create_invoice_table()
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
