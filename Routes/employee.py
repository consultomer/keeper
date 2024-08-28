from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required

from Scripts.Database.employee import 

employee_bp = Blueprint("employee", __name__)


@employee_bp.route("/add")
@login_required
def employeeadd():
    return render_template("addemployee.html")


@employee_bp.route("/edit")
@login_required
def employeeedit():
    return render_template("employee.html")


@employee_bp.route("/")
@login_required
def employeelist():
    data = list_invoices()
    return render_template("employee.html", data=data)


@employee_bp.route("/delete/<value>")
@login_required
def employeedelete(value):
    res = delete_employee(value)
    flash(res, category="success")
    return redirect(url_for("employee.employeelist"))

