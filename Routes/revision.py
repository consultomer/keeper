from datetime import datetime
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
import json


from Scripts.Database.invoice import (
    list_invoices,
    edit_invoices,
)
from Scripts.Database.revision import add_revision, list_revision, list_reason, add_reason, delete_reason, edit_reason
from Scripts.Database.dispatch import (
    add_dispatch,
    list_dispatches,
    view_dispatch,
    delete_dispatch,
)

revision_bp = Blueprint("revision", __name__)


@revision_bp.route("/")
@login_required
def revisionlist():
    if request.args.get("sort_by") and request.args.get("sort_order"):
        sort_order = request.args.get("sort_order").upper()
    else:
        sort_order = "asc"
    sort_by = request.args.get("sort_by")
    status = False
    data = list_invoices(sort_by, sort_order, status)
    revision = list_revision()
    if data == False:
        mess = "No Data"
        flash(mess, category="error")
        data = []
        sort_by = ""
        sort_order = ""
    return render_template(
        "Revision/list.html",
        current=current_user,
        data=data,
        revision=revision,
        sort_by=sort_by,
        sort_order=sort_order.lower(),
    )


@revision_bp.route("/add", methods=["POST", "GET"])
@login_required
def addrevision():
    if request.method == "POST":
        data = request.form  # Get the form data

        # Get the lists of invoice IDs, revisions, and reasons
        invoice_ids = data.getlist("invoice[]")
        revisions = data.getlist("revision[]")
        reasons = data.getlist("reason[]")
        # Ensure all lists have the same length
        if len(invoice_ids) == len(revisions) == len(reasons):
            res = add_revision(invoice_ids, revisions, reasons)
            if res:
                flash("Revisions Added Successfully", category="success")
            else:
                flash("Revisions Adding Error", category="error")
        else:
            flash("Error: Mismatched input data", category="error")

        return redirect(url_for("revision.revisionlist"))

    else:
        if request.args.get("sort_by") and request.args.get("sort_order"):
            sort_order = request.args.get("sort_order").upper()
        else:
            sort_order = "asc"
        sort_by = request.args.get("sort_by")
        status = False
        data = list_invoices(sort_by, sort_order, status)

        reasons = list_reason()
        return render_template("Revision/add.html", current=current_user, data=data, reasons=reasons)
    

    

@revision_bp.route("/reason", methods=["POST", "GET"])
@login_required
def reasonlist():
    if request.method == "POST":
        data = request.form
        reason = data["reason"]
        add_reason(reason)
        flash("Reason Added", category="success")
        return redirect(url_for("revision.reasonlist"))
    else:
        reasons = list_reason()
        return render_template("Revision/reason.html", current=current_user, reasons=reasons)


@revision_bp.route("/edit/<int:value>", methods=["POST", "GET"])
@login_required
def reasonedit(value):
    if request.method == "POST":
        data = request.get_json()  
        reason = data.get("reason")
        edit_reason(value, reason)
        flash("Reason Edited", category="success")
        return redirect(url_for("revision.reasonlist"))
    else:
        reasons = list_reason()
        return render_template("Revision/reason.html", current=current_user, reasons=reasons)


@revision_bp.route("/delete/<int:value>", methods=["POST", "GET"])
@login_required
def reasondel(value):
    if request.method == "GET":
        delete_reason(value)
        flash("Reason Deleted", category="success")
        return redirect(url_for("revision.reasonlist"))
    else:
        reasons = list_reason()
        return render_template("Revision/reason.html", current=current_user, reasons=reasons)
    
