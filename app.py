from flask import Flask
import os

from Scripts.Database.db import init_db
from Scripts.extensions import login_manager
from Routes.customer import customer_bp
from Routes.employee import employee_bp
from Routes.invoice import invoice_bp
from Routes.payment import payment_bp
from Routes.dispatch import dispatch_bp
from Routes.Auth import auth_bp
from Routes.routes import route_bp
from Routes.user import user_bp

app = Flask(__name__)
app.secret_key = os.environ.get("SCERET_KEY")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


init_db(app)


login_manager.login_view = "auth.login"
login_manager.init_app(app)

dropbox = "sl.B71AehdLYDfgEsRAVMqg6uuMU_2DQHCJy-hDxCjT_mpMJGMyUJr72AJiUAO6GaRu4ErK75HcUrdfQ3tcg189g9JPN2DOJ5NvwneToJLf2EBjvjNVg-5gBIhmjid2lpIdO41LmDhCeKWI"
app.register_blueprint(route_bp, url_prefix="/")
app.register_blueprint(customer_bp, url_prefix="/customer")
app.register_blueprint(employee_bp, url_prefix="/employee")
app.register_blueprint(invoice_bp, url_prefix="/invoice")
app.register_blueprint(payment_bp, url_prefix="/payment")
app.register_blueprint(dispatch_bp, url_prefix="/dispatch")
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(user_bp, url_prefix="/user")
