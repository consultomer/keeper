from flask import Blueprint, render_template
from datetime import datetime, timedelta
import jwt, bcrypt


invoice_bp = Blueprint("invoice", __name__)

@invoice_bp.route("/add")
def invoiceadd():
    return render_template("addinvoice.html")


@invoice_bp.route("/edit")
def invoiceedit():
    return render_template("invoice.html")


@invoice_bp.route("/")
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
def invoicedelete():
    return render_template("invoice.html")
