from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required,  current_user


from Scripts.Database.customer import list_customers, delete_customer



customer_bp = Blueprint("customer", __name__)


@customer_bp.route("/")
@login_required
def customerlist():
    data = list_customers()
    return render_template("customer.html", current= current_user, data=data)

@customer_bp.route("/<value>")
@login_required
def singlecus():
    print("OOPs")


@customer_bp.route("/add", methods=["GET", "POST"])
@login_required
def customeradd():
    return render_template("addcustomer.html")


@customer_bp.route("/edit/<value>", methods=["GET", "POST"])
@login_required
def customeredit():
    return render_template("customer.html")




@customer_bp.route("/delete/<value>", methods=["GET"])
@login_required
def customerdelete(value):
    res = delete_customer(value)
    if res == True:
        mess = "Customer Deleted Successfully"
        flash(mess, category="success")
        return redirect(url_for('customer.costumerlist'))
    else:
        flash(res, category="error")
        return redirect(url_for('customer.costumerlist'))
