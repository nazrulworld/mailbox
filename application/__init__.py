from flask import Flask
from flask.ext.wtf.csrf import CsrfProtect

app = Flask(__name__, static_folder='static')
app.config.from_object('config.application')
CsrfProtect(app)
