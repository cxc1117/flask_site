from flask import render_template, flash, redirect, url_for, request, send_from_directory
from app import app, db
from app.forms import NewUserRegistrationForm, LoginForm
from app.models import User, Role, UserRoles
from datetime import datetime
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
from werkzeug.utils import secure_filename
import os
from email_validator import validate_email, EmailNotValidError
from uuid import uuid4


@app.route("/")
def home():
    return render_template("home.html", title="Affiliated")

@app.route("/test/")
def test():
    return render_template("base.html", title ="test")

@app.route("/contact/")
def contact():
    return render_template("contact_us.html", title = "Contact us")

@app.route("/about_us/")
def about_us():
    return render_template("about_us.html", title = "About us")

@app.route("/cases/")
def case_studies():
    return render_template("case_studies.html", title = "Case studies")

@app.route("/login/", methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter((User.username == form.user_or_email.data) | (User.email == form.user_or_email.data)).first()
        if not user or not user.check_password(form.password.data):
            flash("Incorrect username or password, please try again", "danger")
            return redirect(url_for("login"))
        if user.is_active:
            login_user(user, remember=form.remember_me.data)
            flash(f"Login for {user.username} successful!", "success")
            next_page = request.args.get('next')
            if not next_page or urlsplit(next_page).netloc != "":
                next_page = url_for("home")
            return redirect(next_page)
        else:
            flash("User account is currently inactive, please contact an administrator if this is a mistake", "danger")
            return redirect(url_for("home"))
    return render_template("login.html", form=form, title="Login")


@app.route("/register/", methods = ["GET", "POST"])
def register_user_account():
    form = NewUserRegistrationForm()
    if form.validate_on_submit():
        new_user = User(username = form.username.data, email = form.email.data)
        new_user.set_password(form.password_verified.data)
        new_user.set_user_role()
        db.session.add(new_user)
        try:
            db.session.commit()
            flash(f"Account successfully created: {form.username.data}", "success")
            return redirect(url_for("home"))
        except:
            db.session.rollback()
            if User.query.filter_by(username = form.username.data).first():
                form.username.errors.append("This username is already taken, please choose another")
            if User.query.filter_by(email = form.email.data).first():
                form.email.errors.append("This Email address is already registered, please choose another or Login")
    return render_template("register_user_account.html", title="Register new user account", form=form)


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


def is_valid_email(email):
    try:
        validate_email(email, check_deliverability=False)
    except EmailNotValidError as error:
        return False
    return True


def silent_remove(filepath):
    try:
        os.remove(filepath)
    except:
        pass
    return


# @app.errorhandler(413)
# def error_413():
#     return render_template("errors/413.html"), 413