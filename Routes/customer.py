from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required

from Scripts.Database.customer import list_customers, delete_customer

customer_bp = Blueprint("customer", __name__)


@customer_bp.route("/add")
@login_required
def customeradd():
    return render_template("addcustomer.html")


@customer_bp.route("/edit")
@login_required
def customeredit():
    return render_template("customer.html")


@customer_bp.route("/")
@login_required
def customerlist():
    data = list_customers()
    return render_template("customer.html", data=data)


@customer_bp.route("/delete/<value>")
@login_required
def customerdelete(value):
    res = delete_customer(value)
    flash(res, category="success")
    return redirect(url_for("customer.costumerlist"))
