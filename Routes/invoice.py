from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user


from Scripts.Database.invoice import list_invoices, delete_invoice



invoice_bp = Blueprint("invoice", __name__)


@invoice_bp.route("/")
@login_required
def invoicelist():
    data = list_invoices()
    return render_template("invoice.html", current=current_user, data=data)


@invoice_bp.route("/<value>", methods=["GET", "POST"])
@login_required
def singleinv(value):
    return render_template("addinvoice.html")


@invoice_bp.route("/add", methods=["GET", "POST"])
@login_required
def invoiceadd():
    return render_template("addinvoice.html")


@invoice_bp.route("/edit/<value>", methods=["GET", "POST"])
@login_required
def invoiceedit(value):
    return render_template("invoice.html")



@invoice_bp.route("/delete/<value>", methods=["GET"])
@login_required
def invoicedelete(value):
    res = delete_invoice(value)
    if res == True:
        mess = "Bill Deleted Successfully"
        flash(mess, category="success")
        return redirect(url_for("invoice.invoicelist"))
    else:
        flash(res, category="error")
        return redirect(url_for("invoice.invoicelist"))
