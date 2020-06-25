from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import (
    DataRequired,
    Length,
    Email
)
from wtforms.widgets import HiddenInput


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name',  validators=[DataRequired(), Length(max=255)])
    last_name = StringField('Last Name',  validators=[DataRequired(), Length(max=255)])
    email = StringField('Email',  validators=[Email(), Length(max=255)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=255)])


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(max=255)])
    password = PasswordField('Password',  validators=[DataRequired(), Length(max=255)])
    remember = BooleanField('Remember me', default=False)
