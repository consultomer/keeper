from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user


from Scripts.Database.employee import delete_employee, list_employees


employee_bp = Blueprint("employee", __name__)


@employee_bp.route("/")
@login_required
def employeelist():
    data = list_employees()
    if data == False:
        mess = "No Data"
        flash(mess, category="error")
        data = []
    return render_template("employee.html", current=current_user, data=data)


@employee_bp.route("/edit/<value>")
@login_required
def singleemp(value):
    print("lol")


@employee_bp.route("/add", methods=["GET", "POST"])
@login_required
def employeeadd():
    return render_template("addemployee.html")


@employee_bp.route("/edit/<value>", methods=["GET", "POST"])
@login_required
def employeeedit(value):
    return render_template("employee.html")


@employee_bp.route("/delete/<value>", methods=["GET"])
@login_required
def employeedelete(value):
    res = delete_employee(value)
    if res == True:
        mess = "Employee Deleted Successfully"
        flash(mess, category="success")
        return redirect(url_for("employee.employeelist"))
    else:
        flash(res, category="error")
        return redirect(url_for("employee.employeelist"))
