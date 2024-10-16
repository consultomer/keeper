from datetime import datetime
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
import json


from Scripts.Database.invoice import (
    sininvoice,
    edit_invoices,
)
from Scripts.Database.employee import employee
from Scripts.Database.dispatch import (
    add_dispatch,
    list_dispatches,
    view_dispatch,
    delete_dispatch,
)

dispatch_bp = Blueprint("dispatch", __name__)


@dispatch_bp.route("/")
@login_required
def dispatchlist():
    # Handle sorting logic based on request arguments, with default sort order being 'ASC'
    sort_order = request.args.get("sort_order", "asc").upper()
    sort_by = request.args.get("sort_by")

    # Fetch dispatch data, sorted accordingly
    data = list_dispatches(sort_by, sort_order)

    # Iterate through each dispatch to calculate totals, paid amounts, revisions, and remaining amounts
    for dispatch in data:
        if isinstance(dispatch["invoices"], str):
            dispatch["invoices"] = json.loads(dispatch["invoices"])

        # Calculate total, paid, revision, and remaining amounts
        total = sum(invoice.get("total", 0) for invoice in dispatch["invoices"])  # Default to 0 if None
        paid = sum(invoice.get("paid", 0) for invoice in dispatch["invoices"])  # Default to 0 if None
        revision = sum(invoice.get("revision_sum", 0) for invoice in dispatch["invoices"])  # Using the summed revisions

        dispatch["total"] = total
        dispatch["paid"] = paid
        dispatch["revision"] = revision
        dispatch["remaining"] = total - paid + revision

    # Handle the case where no data is returned
    if not data:
        mess = "No Data"
        flash(mess, category="error")
        data = []
        sort_by = ""
        sort_order = ""

    return render_template(
        "Dispatch/list.html",
        current=current_user,
        data=data,
        sort_by=sort_by,
        sort_order=sort_order.lower(),
    )



@dispatch_bp.route("/<value>", methods=["GET", "POST"])
@login_required
def singledis(value):
    val = int(value)
    dispatch_data = view_dispatch(val)

    if isinstance(dispatch_data["invoices"], str):
        dispatch_data["invoices"] = json.loads(dispatch_data["invoices"])

    total = 0
    for invoice in dispatch_data["invoices"]:
        total_amount = invoice["total"] if invoice["total"] is not None else 0
        paid_amount = invoice["paid"] if invoice["paid"] is not None else 0
        remain = total_amount - paid_amount + invoice["revision_sum"]  # Include revision sum in remaining
        invoice["remaining"] = remain
        total += remain
    
    dispatch_data["total"] = total

    return render_template(
        "Dispatch/view.html", current=current_user, data=dispatch_data
    )


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
            "Dispatch/add.html",
            current=current_user,
            data=inv_data,
            main=main_data,
            employee=emp,
        )


@dispatch_bp.route("/added", methods=["POST"])
@login_required
def dispatchadd():
    if request.method == "POST":
        delivery_man = request.form.get("delivery_man")
        invoice_ids = request.form.getlist("invoice_ids[]")
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
        form_data = request.form

        # Iterate through the form data to get updated values for each invoice
        invoices = []
        for invoice_id in form_data.getlist("invoice_id"):
            paid = float(form_data.get(f"paid_{invoice_id}", 0))
            status = form_data.get(f"delivery_status_{invoice_id}")

            # Fetch all revision amounts and reasons for the current invoice
            revision_amounts = form_data.getlist(f"revision_{invoice_id}[]")
            revision_reasons = form_data.getlist(f"reason_{invoice_id}[]")

            revisions = []
            for amount, reason in zip(revision_amounts, revision_reasons):
                if amount and reason:
                    try:
                        revisions.append({
                            "revision": float(amount),
                            "revision_reason": reason
                        })
                    except ValueError:
                        flash(f"Invalid revision amount for Invoice ID {invoice_id}.", category="error")
                        return redirect(url_for("dispatch.dispatchedit", value=value))

            invoices.append(
                {
                    "invoice_id": int(invoice_id),
                    "paid": paid,
                    "revision": revisions,
                    "delivery": status,
                }
            )

        # Assuming you have a function to update the invoices in the database
        res = edit_invoices(invoices)
        if res == True:
            flash("Hisaab edit Successfully", category="success")
            return redirect(url_for("dispatch.dispatchlist"))
        else:
            flash(res, category="error")
            val = int(value)
            dispatch_data = view_dispatch(val)

            if isinstance(dispatch_data["invoices"], str):
                dispatch_data["invoices"] = json.loads(dispatch_data["invoices"])
            total = 0
            for invoice in dispatch_data["invoices"]:
                total_amount = invoice["total"] if invoice["total"] is not None else 0
                paid_amount = invoice["paid"] if invoice["paid"] is not None else 0
                remain = total_amount - paid_amount
                invoice["remaining"] = remain
                total += remain
            dispatch_data["total"] = total

            return render_template(
                "Dispatch/edit.html", current=current_user, data=dispatch_data
            )

    else:
        val = int(value)
        dispatch_data = view_dispatch(val)

        if isinstance(dispatch_data["invoices"], str):
            dispatch_data["invoices"] = json.loads(dispatch_data["invoices"])
        total = 0
        for invoice in dispatch_data["invoices"]:
            total_amount = invoice["total"] if invoice["total"] is not None else 0
            paid_amount = invoice["paid"] if invoice["paid"] is not None else 0
            remain = total_amount - paid_amount
            invoice["remaining"] = remain
            total += remain
        dispatch_data["total"] = total
        # return dispatch_data
        return render_template(
            "Dispatch/edit.html", current=current_user, data=dispatch_data
        )


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
