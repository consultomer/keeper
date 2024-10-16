from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user


from Scripts.Database.invoice import (
    list_invoices,
    add_invoice,
    sininvoice,
    single_invoice,
    edit_invoice,
    delete_invoice,
)
from Scripts.Database.employee import employee
from Scripts.Database.customer import customer

invoice_bp = Blueprint("invoice", __name__)


@invoice_bp.route("/")
@login_required
def invoicelist():
    if request.args.get("sort_by") and request.args.get("sort_order"):
        sort_order = request.args.get("sort_order").upper()
    else:
        sort_order = "asc"
    sort_by = request.args.get("sort_by")
    status = False
    data = list_invoices(sort_by, sort_order, status)
    if data == False:
        mess = "No Data"
        flash(mess, category="error")
        data = []
        sort_by = ""
        sort_order = ""
    return render_template(
        "Invoices/list.html",
        current=current_user,
        data=data,
        sort_by=sort_by,
        sort_order=sort_order.lower(),
    )


@invoice_bp.route("/delivered")
@login_required
def deinvoicelist():
    if request.args.get("sort_by") and request.args.get("sort_order"):
        sort_order = request.args.get("sort_order").upper()
    else:
        sort_order = "asc"
    sort_by = request.args.get("sort_by")
    status = True
    data = list_invoices(sort_by, sort_order, status)
    if data == False:
        mess = "No Data"
        flash(mess, category="error")
        data = []
        sort_by = ""
        sort_order = ""
    return render_template(
        "Invoices/delivered.html",
        current=current_user,
        data=data,
        sort_by=sort_by,
        sort_order=sort_order.lower(),
    )


@invoice_bp.route("/<value>", methods=["GET", "POST"])
@login_required
def singleinv(value):
    val = int(value)
    inv = sininvoice(val)
    if inv:
        total = inv["total"] or 0
        paid = inv["paid"] or 0
        revision = 0
        for rev in inv["revisions"]:
            revision += rev["revision"]
        inv["remaining"] = total - paid + revision
    return render_template("Invoices/view.html", current=current_user, invoice=inv)


@invoice_bp.route("/add", methods=["GET", "POST"])
@login_required
def invoiceadd():
    if request.method == "POST":
        data = request.form

        # Extract data from form
        bookers = data.getlist("booker[]")
        dsrs = data.getlist("dsr[]")
        customers = data.getlist("customer[]")
        values = data.getlist("value[]")
        dates = data.getlist("date[]")

        # Iterate through the data and process each invoice
        for booker, dsr, custom, value, date in zip(
            bookers, dsrs, customers, values, dates
        ):
            inv_data = {
                "booker": booker,
                "dsr": dsr,
                "customer_id": custom,
                "total": value,
                "date": date,
            }
            res = add_invoice(inv_data)
            if res is not True:
                flash(res, category="error")
                return redirect(url_for("invoice.invoiceadd"))

        flash("Invoice(s) Added Successfully", category="success")
        return redirect(url_for("invoice.invoicelist"))
    else:
        emp = employee()
        cust = customer()
        return render_template(
            "Invoices/add.html", current=current_user, employee=emp, customer=cust
        )


@invoice_bp.route("/edit/<int:value>", methods=["GET", "POST"])
@login_required
def invoiceedit(value):
    if request.method == "POST":
        data = request.form
        invoice_data = {
            "invoice_id": value,
            "booker": data.get("booker"),
            "delivery_man": data.get("delivery_man"),
            "dsr": data.get("dsr"),
            "customer_id": data.get("customer"),
            "total": data.get("total"),
            "paid": data.get("paid"),
            "company": data.get("company"),
            "delivery_status": data.get("delivery_status"),
            "payment_status": data.get("payment_status"),
        }
        res = edit_invoice(invoice_data)
        if res == True:
            flash("Invoice edit Successfully", category="success")
            return redirect(url_for("invoice.invoicelist"))
        else:
            flash(res, category="error")
            inv = invoice_data
            emp = employee()
            cust = customer()
            return render_template(
                "Invoices/edit.html",
                current=current_user,
                invoice=inv,
                customer=cust,
                employee=emp,
            )

    else:
        val = int(value)
        inv = single_invoice(val)[0]
        emp = employee()
        cust = customer()

        return render_template(
            "Invoices/edit.html",
            current=current_user,
            invoice=inv,
            customer=cust,
            employee=emp,
        )


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
