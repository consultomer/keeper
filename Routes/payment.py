
from flask import Blueprint, render_template
from flask_login import login_required
from datetime import datetime, timedelta
import jwt, bcrypt


payment_bp = Blueprint("payment", __name__)

@payment_bp.route("/add")
@login_required
def paymentadd():
    return render_template("payment.html")


@payment_bp.route("/edit")
@login_required
def paymentedit():
    return render_template("payment.html")


@payment_bp.route("/")
@login_required
def paymentlist():
    return render_template("payment.html")


@payment_bp.route("/delete")
@login_required
def paymentdelete():
    return render_template("payment.html")
