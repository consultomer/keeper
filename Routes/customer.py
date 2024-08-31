from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required,  current_user
from werkzeug.utils import secure_filename


from Scripts.Database.customer import list_customers, find_customer, add_customer, edit_customer, delete_customer
from Scripts.encryptions import process_csv, process_xlsx

ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


customer_bp = Blueprint("customer", __name__)


@customer_bp.route("/")
@login_required
def customerlist():
    page = request.args.get('page', 1, type=int)
    per_page = 20  # Number of items per page
    
    # Fetch paginated data
    data, total_count = list_customers(page, per_page)
    
    if not data and total_count == 0:
        mess = "No Data"
        flash(mess, category="error")
        data = []

    return render_template(
        "Customers/list.html", 
        current=current_user, 
        data=data, 
        page=page, 
        per_page=per_page, 
        total_count=total_count
    )



@customer_bp.route("/<value>")
@login_required
def singlecustomer(value):
    val = int(value)
    cust = find_customer(val)
    return render_template("Customers/view.html", current=current_user, data=cust)


@customer_bp.route("/add", methods=["GET", "POST"])
@login_required
def customeradd():
    if request.method == "POST":
        data = request.form
        customer_data = {
            "business_name": data.get("business_name"),
            "address": data.get("address"),
            "area": data.get("area"),
            "route": data.get("route"),
            "category": data.get("category"),
            "phone": data.get("phone"),
            "whatsapp": data.get("whatsapp"),
            "shop_ownership": data.get("shop_ownership"),
            "cnic": data.get("cnic"),
            "tax_filer_status": data.get("tax_filer_status"),
            "channel": data.get("channel"),
            "class": data.get("class"),
            "business_status": data.get("business_status"),
            "shop_status": data.get("shop_status"),
            "business_health": data.get("business_health"),
        }
        res = add_customer(customer_data)
        if res == True:
            flash("Customer Added Successfully", category="success")
            return redirect(url_for('customer.customerlist'))
        else:
            flash(res, category="error")
            return redirect(url_for('customer.customeradd'))
    else:
        return render_template("Customers/add.html", current=current_user)


@customer_bp.route("/upload", methods=["GET", "POST"])
@login_required
def customerbulk():
    if request.method == "POST":
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = f'Uploads/{filename}'
                file.save(file_path)
                
                if filename.endswith('.csv'):
                    customer_data_list = process_csv(file_path)
                elif filename.endswith('.xlsx'):
                    customer_data_list = process_xlsx(file_path)
                
                # Insert customers into the database
                for customer_data in customer_data_list:
                    res = add_customer(customer_data)
                    if res != True:
                        flash(res, category="error")
                        return redirect(url_for('customer.customerbulk'))
                
                flash("Customers Added Successfully", category="success")
                return redirect(url_for('customer.customerlist'))
            else:
                flash("Invalid file type. Only CSV and XLSX files are allowed.", category="error")
                return render_template("Customers/addbulk.html", current=current_user)
    else:
            return render_template("Customers/addbulk.html", current=current_user)


@customer_bp.route("/edit/<value>", methods=["GET", "POST"])
@login_required
def customeredit(value):
    if request.method == "POST":
        data = request.form
        customer_data = {
            "customer_id": value,
            "business_name": data.get("business_name"),
            "address": data.get("address"),
            "area": data.get("area"),
            "route": data.get("route"),
            "category": data.get("category"),
            "phone": data.get("phone"),
            "whatsapp": data.get("whatsapp"),
            "shop_ownership": data.get("shop_ownership"),
            "cnic": data.get("cnic"),
            "tax_filer_status": data.get("tax_filer_status"),
            "channel": data.get("channel"),
            "class": data.get("class"),
            "business_status": data.get("business_status"),
            "shop_status": data.get("shop_status"),
            "business_health": data.get("business_health"),
        }
        res = edit_customer(customer_data)

        if res == True:
            mess = "Customer edit Successfully"
            flash(mess, category="success")
            return redirect(url_for('customer.customerlist'))
        else:
            flash(res, category="error")
            return redirect(url_for('customer.customeradd'))
    else:
        val = int(value)
        customer = find_customer(val)
        return render_template("Customers/edit.html", current=current_user, data=customer)


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
