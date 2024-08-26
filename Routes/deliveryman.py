from flask import Blueprint, render_template
from datetime import datetime, timedelta
import jwt, bcrypt

delivery_bp = Blueprint("delivery", __name__)

@delivery_bp.route("/add")
def deliveryadd():
    return render_template("adddelman.html")


@delivery_bp.route("/edit")
def deliveryedit():
    return render_template("delivery.html")


@delivery_bp.route("/")
def deliverylist():
    data = [
        {
            "deliveryman_id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "phone_number": 123456,
            "status": "pending",
        },
        {
            "deliveryman_id": 2,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "phone_number": 123456,
            "status": "pending",
        },
        {
            "deliveryman_id": 3,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "phone_number": 123456,
            "status": "pending",
        },
    ]
    return render_template("delivery.html", data=data)


@delivery_bp.route("/delete")
def deliverydelete():
    return render_template("delivery.html")
