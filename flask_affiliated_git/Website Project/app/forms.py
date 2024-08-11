from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo, NumberRange, Length
from app.models import User, UserRoles, Role

class NewUserRegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(1, 24, message="This username exceeds the 24 character limit!")])
    email = StringField("Email address", validators=[DataRequired(), Email(), Length(1, 64)])
    password = PasswordField("Password", validators=[DataRequired()])
    password_verified = PasswordField("Re-enter password", validators=[DataRequired(), EqualTo("password",
                                                            message="Passwords do not match, please try again.")])
    submit = SubmitField("Register Account")
    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("This username is already taken, please try another")
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("This email is already registered, please login or select another.")

class LoginForm(FlaskForm):
    user_or_email = StringField("Username or Email address", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Login")