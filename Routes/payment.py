from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required

from Scripts.Database.payment import list_payments, delete_payment


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
    data = list_payments()
    return render_template("payment.html", data=data)


@payment_bp.route("/delete/<value>")
@login_required
def paymentdelete(value):
    res = delete_payment(value)
    flash(res, category="success")
    return redirect(url_for("payment.paymentlist"))
