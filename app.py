from flask import Flask
import os
from Routes.customer import customer_bp
from Routes.deliveryman import delivery_bp
from Routes.invoice import invoice_bp
from Routes.payment import payment_bp
from Routes.Auth import auth_bp
from Routes.routes import route_bp
from Routes.user import user_bp

app = Flask(__name__)
app.secret_key = os.environ.get('SCERET_KEY')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.register_blueprint(customer_bp, url_prefix="/customer")
app.register_blueprint(delivery_bp, url_prefix="/deliveryman")
app.register_blueprint(invoice_bp, url_prefix="/invoice")
app.register_blueprint(payment_bp, url_prefix="/payment")
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(route_bp, url_prefix="/")
