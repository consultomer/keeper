from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user


from Scripts.Database.invoice import list_invoices, add_invoice, sininvoice, delete_invoice
from Scripts.Database.employee import employee
from Scripts.Database.customer import customer

invoice_bp = Blueprint("invoice", __name__)


@invoice_bp.route("/")
@login_required
def invoicelist():
    data = list_invoices()
    if data == False:
        mess = "No Data"
        flash(mess, category="error")
        data = []
    return render_template("Invoices/list.html", current=current_user, data=data)


@invoice_bp.route("/<value>", methods=["GET", "POST"])
@login_required
def singleinv(value):
    val = int(value)
    inv = sininvoice(value)[0]
    if inv:
        total = inv['total'] or 0
        paid = inv['paid'] or 0
        inv['remaining'] = total - paid
    return render_template("Invoices/view.html", current=current_user, invoice=inv )


@invoice_bp.route("/add", methods=["GET", "POST"])
@login_required
def invoiceadd():
    if request.method == "POST":
        data = request.form
        inv_data = {
            "booker": data.get("booker"),
            "dsr": data.get("dsr"),
            "customer_id": data.get("customer"),
            "total": data.get("value"),
            "company": data.get("company"),
            "delivery_man": data.get("delivery_man")
        }
        res = add_invoice(inv_data)
        if res == True:
            flash("Invoice Added Successfully", category="success")
            return redirect(url_for("invoice.invoicelist"))
        else:
            flash(res, category="error")
            return redirect(url_for("invoice.invoiceadd"))
    else:
        list = employee()
        cust = customer()
        return render_template("Invoices/add.html", current=current_user, employee=list, customer=cust)


@invoice_bp.route("/edit/<value>", methods=["GET", "POST"])
@login_required
def invoiceedit(value):
    return render_template("Invoices/edit.html")


@invoice_bp.route("/delete/<value>", methods=["GET"])
@login_required
def invoicedelete(value):
    res = delete_invoice(value)
    if res == True:
        mess = "Invoice Deleted Successfully"
        flash(mess, category="success")
        return redirect(url_for("invoice.invoicelist"))
    else:
        flash(res, category="error")
        return redirect(url_for("invoice.invoicelist"))
