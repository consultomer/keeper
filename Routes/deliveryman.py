from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required

from Scripts.Database.delivery import list_invoices, delete_invoice

delivery_bp = Blueprint("delivery", __name__)


@delivery_bp.route("/add")
@login_required
def deliveryadd():
    return render_template("adddelman.html")


@delivery_bp.route("/edit")
@login_required
def deliveryedit():
    return render_template("delivery.html")


@delivery_bp.route("/")
@login_required
def deliverylist():
    data = list_invoices()
    return render_template("delivery.html", data=data)


@delivery_bp.route("/delete/<value>")
@login_required
def deliverydelete(value):
    res = delete_delivery(value)
    flash(res, category="success")
    return redirect(url_for("delivery.deliverylist"))

