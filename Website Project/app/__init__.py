import os
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = b"IRMHIWHBSBADZRO1234132fev_123=+{WQw"
login = LoginManager(app)
login.login_view = "login"
login.login_message_category = "danger"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data", "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = os.path.join(basedir, "data", 'uploads')
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024


db = SQLAlchemy(app)

from app import views
from app.models import *

@app.shell_context_processor
def make_shell_context():
    return dict(db = db, datetime = datetime, User = User, UserRoles = UserRoles, Role = Role, LoginManager = LoginManager)

