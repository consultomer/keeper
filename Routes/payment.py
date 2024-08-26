
from flask import Blueprint, render_template
from datetime import datetime, timedelta
import jwt, bcrypt


payment_bp = Blueprint("payment", __name__)

@payment_bp.route("/add")
def paymentadd():
    return render_template("payment.html")


@payment_bp.route("/edit")
def paymentedit():
    return render_template("payment.html")


@payment_bp.route("/")
def paymentlist():
    return render_template("payment.html")


@payment_bp.route("/delete")
def paymentdelete():
    return render_template("payment.html")
