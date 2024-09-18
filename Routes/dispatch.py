from datetime import datetime
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
import json


from Scripts.Database.invoice import (
    sininvoice,
    single_invoice,
    edit_invoice,
)
from Scripts.Database.employee import employee
from Scripts.Database.customer import customer
from Scripts.Database.dispatch import add_dispatch, list_dispatches, view_dispatch, delete_dispatch

dispatch_bp = Blueprint("dispatch", __name__)


@dispatch_bp.route("/")
@login_required
def dispatchlist():
    if request.args.get("sort_by") and request.args.get("sort_order"):
        sort_order = request.args.get("sort_order").upper()
    else:
        sort_order = "asc"
    sort_by = request.args.get("sort_by")
    data = list_dispatches(sort_by, sort_order)
    for dispatch in data:
        if isinstance(dispatch['invoices'], str):
            dispatch['invoices'] = json.loads(dispatch['invoices'])
        total = sum(invoice['total'] for invoice in dispatch['invoices'])
        dispatch['total'] = total
    if data == False:
        mess = "No Data"
        flash(mess, category="error")
        data = []
        sort_by = ""
        sort_order = ""

    return render_template("Dispatch/list.html", current=current_user, data=data, sort_by=sort_by, sort_order=sort_order.lower())


@dispatch_bp.route("/<value>", methods=["GET", "POST"])
@login_required
def singledis(value):
    val = int(value)
    dispatch_data = view_dispatch(val)
    
    if isinstance(dispatch_data['invoices'], str):
        dispatch_data['invoices'] = json.loads(dispatch_data['invoices'])
    total = 0
    for invoice in dispatch_data['invoices']:
        total_amount = invoice['total'] if invoice['total'] is not None else 0
        paid_amount = invoice['paid'] if invoice['paid'] is not None else 0
        remain = total_amount - paid_amount
        invoice['remaining'] = remain
        total += remain
    dispatch_data['total'] = total
    # return dispatch_data
    return render_template('Dispatch/view.html', current=current_user, data=dispatch_data)



@dispatch_bp.route("/add", methods=["POST"])
@login_required
def invoiceadd():
    if request.method == "POST":
        data = request.form
        inv_data = []
        main_data = {
            "total": 0,
            "date": datetime.now().date(),
        }

        for d in data.values():
            inv_daa = sininvoice(int(d))[0]
            if inv_daa:  # Ensure inv_daa is not None
                total = inv_daa.get("total", 0) or 0
                main_data["total"] += total
                inv_data.append(inv_daa)
        emp = employee()
        return render_template(
            "Dispatch/add.html", current=current_user, data=inv_data, main=main_data, employee=emp
        )


@dispatch_bp.route("/added", methods=["POST"])
@login_required
def dispatchadd():
    if request.method == "POST":
        delivery_man = request.form.get('delivery_man')
        invoice_ids = request.form.getlist('invoice_ids[]')
        res = add_dispatch(delivery_man, invoice_ids)
        if res == True:
            flash("Dispatch Created Successfully", category="success")
            return redirect(url_for("dispatch.dispatchlist"))
        else:
            flash(res, category="error")
            return redirect(url_for("invoice.invoicelist"))



@dispatch_bp.route("/edit/<int:value>", methods=["GET", "POST"])
@login_required
def dispatchedit(value):
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
            "revision": data.get("revision"),
            "delivery_status": data.get("delivery_status"),
            "payment_status": data.get("payment_status"),
            "notes": data.get("notes"),
        }
        return data
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
                "Dispatch/edit.html",
                current=current_user,
                invoice=inv,
                customer=cust,
                employee=emp,
            )

    else:
        val = int(value)
        dispatch_data = view_dispatch(val)
        
        if isinstance(dispatch_data['invoices'], str):
            dispatch_data['invoices'] = json.loads(dispatch_data['invoices'])
        total = 0
        for invoice in dispatch_data['invoices']:
            total_amount = invoice['total'] if invoice['total'] is not None else 0
            paid_amount = invoice['paid'] if invoice['paid'] is not None else 0
            remain = total_amount - paid_amount
            invoice['remaining'] = remain
            total += remain
        dispatch_data['total'] = total
        # return dispatch_data
        return render_template('Dispatch/edit.html', current=current_user, data=dispatch_data)


@dispatch_bp.route("/delete/<value>", methods=["GET"])
@login_required
def disdelete(value):
    res = delete_dispatch(value)
    if res == True:
        mess = "Dispatch Deleted Successfully"
        flash(mess, category="success")
        return redirect(url_for("dispatch.dispatchlist"))
    else:
        flash(res, category="error")
        return redirect(url_for("dispatch.dispatchlist"))
