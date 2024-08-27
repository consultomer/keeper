from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required

from Scripts.Database.invoice import list_invoices, delete_invoice


invoice_bp = Blueprint("invoice", __name__)


@invoice_bp.route("/add")
@login_required
def invoiceadd():
    return render_template("addinvoice.html")


@invoice_bp.route("/edit")
@login_required
def invoiceedit():
    return render_template("invoice.html")


@invoice_bp.route("/")
@login_required
def invoicelist():
    data = list_invoices()
    return render_template("invoice.html", data=data)


@invoice_bp.route("/delete/<value>")
@login_required
def invoicedelete(value):
    res = delete_invoice(value)
    flash(res, category="success")
    return redirect(url_for("invoice.invoicelist"))
