from flask import Blueprint, render_template
from flask_login import login_required
from datetime import datetime, timedelta
import jwt, bcrypt


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
    data = [
        {
            "invoice_id": 1,
            "customer_id": 1,
            "invoice_amount": 123456,
            "payment_status": "pending",
            "delivery_status": "pending",
            "updated_at": datetime.now()
        },
        {
            "invoice_id": 1,
            "customer_id": 1,
            "invoice_amount": 123456,
            "payment_status": "pending",
            "delivery_status": "pending",
            "updated_at": datetime.now()
        },
        {
            "invoice_id": 1,
            "customer_id": 1,
            "invoice_amount": 123456,
            "payment_status": "pending",
            "delivery_status": "pending",
            "updated_at": datetime.now()
        },
        {
            "invoice_id": 1,
            "customer_id": 1,
            "invoice_amount": 123456,
            "payment_status": "pending",
            "delivery_status": "pending",
            "updated_at": datetime.now()
        },
        {
            "invoice_id": 1,
            "customer_id": 1,
            "invoice_amount": 123456,
            "payment_status": "pending",
            "delivery_status": "pending",
            "updated_at": datetime.now()
        }
    ]
    return render_template("invoice.html", data=data)


@invoice_bp.route("/delete")
@login_required
def invoicedelete():
    return render_template("invoice.html")
