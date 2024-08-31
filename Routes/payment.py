from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from Scripts.Database.payment import list_payments, delete_payment




payment_bp = Blueprint("payment", __name__)


@payment_bp.route("/")
@login_required
def paymentlist():
    data = list_payments()
    if data == False:
        mess = "No Data"
        flash(mess, category="error")
        data = []
    return render_template("payment.html", current=current_user, data=data)


@payment_bp.route("/<value>")
@login_required
def singlepay(value):
    print("llll")


@payment_bp.route("/add", methods=["GET", "POST"])
@login_required
def paymentadd():
    return render_template("payment.html")


@payment_bp.route("/edit/<value>", methods=["GET", "POST"])
@login_required
def paymentedit():
    return render_template("payment.html")




@payment_bp.route("/delete/<value>", methods=["GET"])
@login_required
def paymentdelete(value):
    res = delete_payment(value)
    if res == True:
        mess = "Bill Deleted Successfully"
        flash(mess, category="success")
        return redirect(url_for('payment.paymentlist'))
    else:
        flash(res, category="error")
        return redirect(url_for('payment.paymentlist'))
