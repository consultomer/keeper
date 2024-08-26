from flask import Flask
import os


app = Flask(__name__)
app.secret_key = os.environ.get('SCERET_KEY')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
from Routes import routes