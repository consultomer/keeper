import re
import csv
import openpyxl


def password_is_valid(password):
    if isinstance(password, bytes):
        password = password.decode("utf-8")
    if len(password) <= 7:
        return False, "Password must be longer than 7 characters."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one numeric character."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase character."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase character."
    if not re.search(r"[@$!%*?&#]", password):
        return False, "Password must contain at least one special character (@$!%*?&#)."
    return True, ""


def process_csv(file_path):
    customer_data_list = []
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            customer_data = {
                "business_name": row["business_name"],
                "address": row["address"],
                "area": row["area"],
                "route": row["route"],
                "category": row["category"],
                "phone": row["phone"],
                "whatsapp": row["whatsapp"],
                "shop_ownership": row["shop_ownership"],
                "cnic": row["cnic"],
                "tax_filer_status": row["tax_filer_status"],
                "channel": row["channel"],
                "class": row["class"],
                "business_status": row["business_status"],
                "shop_status": row["shop_status"],
                "business_health": row["business_health"],
            }
            customer_data_list.append(customer_data)
    return customer_data_list


def process_xlsx(file_path):
    customer_data_list = []
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active
    headers = [cell.value for cell in sheet[1]]

    for row in sheet.iter_rows(min_row=2, values_only=True):
        customer_data = {headers[i]: row[i] for i in range(len(headers))}
        customer_data_list.append(customer_data)

    return customer_data_list
