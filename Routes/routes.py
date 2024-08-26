from app import app
from flask import jsonify, request, render_template
from Scripts.Database.db import create_credit_table, create_customer_table, create_deliverylog_table, create_deliveryman_table, create_invoice_adj_table, create_invoice_table, create_orderbooker_table, create_payment_table, create_users_table
import os, jwt

from flask_cors import CORS

cors = CORS(app, supports_credentials=True)

# login_manager = LoginManager(app)
# login_manager.login_view = "login"



# ------------------ Home ------------------ #
@app.route("/")
# @login_required
def home():
    return render_template("base.html")
    return jsonify({"message": "Backend-Running"})

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/users")
def useer():
    return render_template("users.html")

@app.route("/form")
def formss():
    return render_template("form.html")


# ------------------ Random ------------------ #
@app.route("/api/createtable", methods=["GET"])
def ct():
    res = create_users_table()
    res1 = create_invoice_table()
    res3 = create_customer_table()
    res4 = create_payment_table()
    res5 = create_orderbooker_table()
    res6 = create_credit_table()
    res7 = create_deliverylog_table()
    res8 = create_deliveryman_table()
    res9 = create_invoice_adj_table()

    return jsonify(
        {
            "message": [
                res,
                res1,
                res3,
                res4,
                res5,
                res6,
                res7,
                res8,
                res9
            ]
        }
    )
