from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user


from Scripts.Database.employee import (
    list_employees,
    find_employee,
    add_employee,
    edit_employee,
    delete_employee,
)


employee_bp = Blueprint("employee", __name__)


@employee_bp.route("/")
@login_required
def employeelist():
    page = request.args.get("page", 1, type=int)
    per_page = 20  # Number of items per page

    # Fetch paginated data
    data, total_count = list_employees(page, per_page)

    if not data and total_count == 0:
        mess = "No Data"
        flash(mess, category="error")
        data = []

    return render_template(
        "Employees/list.html",
        current=current_user,
        data=data,
        page=page,
        per_page=per_page,
        total_count=total_count,
    )


@employee_bp.route("/<value>")
@login_required
def singleemp(value):
    val = int(value)
    emp = find_employee(val)
    return render_template("Employees/view.html", current=current_user, data=emp)


@employee_bp.route("/add", methods=["GET", "POST"])
@login_required
def employeeadd():
    if request.method == "POST":
        data = request.form
        emp_data = {
            "name": data.get("name"),
            "role": data.get("role"),
            "phone_number": data.get("phone_number"),
            "whatsapp_number": data.get("whatsapp_number"),
            "address": data.get("address"),
            "company": data.get("company"),
        }
        res = add_employee(emp_data)
        if res == True:
            flash("Employee Added Successfully", category="success")
            return redirect(url_for("employee.employeelist"))
        else:
            flash(res, category="error")
            return redirect(url_for("employee.employeeadd"))
    else:
        return render_template("Employees/add.html", current=current_user)


@employee_bp.route("/edit/<value>", methods=["GET", "POST"])
@login_required
def employeeedit(value):
    if request.method == "POST":
        data = request.form
        emp_data = {
            "employee_id": value,
            "name": data.get("name"),
            "role": data.get("role"),
            "phone_number": data.get("phone_number"),
            "whatsapp_number": data.get("whatsapp_number"),
            "address": data.get("address"),
            "company": data.get("company"),
        }
        res = edit_employee(emp_data)
        if res == True:
            flash("Employee edit Successfully", category="success")
            return redirect(url_for("employee.employeelist"))
        else:
            flash(res, category="error")
            return redirect(url_for("employee.employeeadd"))
    else:
        val = int(value)
        emplo = find_employee(val)
        return render_template("Employees/edit.html", current=current_user, data=emplo)


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
