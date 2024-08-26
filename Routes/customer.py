from flask import Blueprint, render_template
from datetime import datetime, timedelta
import jwt, bcrypt

customer_bp = Blueprint("customer", __name__)


@customer_bp.route("/add")
def customeradd():
    return render_template("addcustomer.html")


@customer_bp.route("/edit")
def customeredit():
    return render_template("customer.html")


@customer_bp.route("/")
def customerlist():
    data = [
        {
            "customer_id": "1",
            "customer_name": "John",
            "customer_email": "john@example.com",
            "customer_mobile": "123456789",
            "customer_address": "1234, Example Street, Example City, Example Country",
            "created_by": "1",
        },
        {
            "customer_id": "2",
            "customer_name": "omer",
            "customer_email": "johnaa@example.com",
            "customer_mobile": "123456789",
            "customer_address": "1234, Example Street, Example City, Example Country",
            "created_by": "1",
        },
        {
            "customer_id": "3",
            "customer_name": "ali",
            "customer_email": "johaan@example.com",
            "customer_mobile": "123456789",
            "customer_address": "1234, Example Street, Example City, Example Country",
            "created_by": "1",
        },
    ]
    return render_template("customer.html", data=data)


@customer_bp.route("/delete")
def customerdelete():
    return render_template("customer.html")
