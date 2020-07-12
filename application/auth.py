from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_user, logout_user, current_user, login_required

from application.extensions import db
from application.email import send_email
from application.helpers.errors import flash_errors
from application.helpers.forms import RegistrationForm, LoginForm, ResetPasswordForm, EmailForm
from application.models import User
from application.token import generate_confirmation_token, confirm_token

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = True if form.remember.data else False

        user = User.auth(email=email, password=password)

        if not user:
            flash("Please check your login details and try again.")
            return redirect(url_for("auth.login"))

        login_user(user=user, remember=remember)
        return redirect(url_for("main.profile"))
    return render_template("login.html", form=form)


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("Email address already exists.")
            return redirect(url_for("auth.register"))

        payload = {
            "first_name": form.first_name.data,
            "last_name": form.last_name.data,
            "email": form.email.data,
            "password": form.password.data,
        }
        user = User(**payload)

        # add the new user to the database
        db.session.add(user)
        db.session.commit()

        token = generate_confirmation_token(user.email)
        send_email(
            redirect="auth.confirm_email",
            html="activate.html",
            recipients=user.email,
            subject="Please confirm your email",
            token=token
        )

        login_user(user)
        flash("A confirmation email has been sent via email.")

        return redirect(url_for("auth.unconfirmed"))
    else:
        flash_errors(form)

    return render_template("register.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@bp.route("/confirm/<string:token>")
@login_required
def confirm_email(token):
    email = confirm_token(token)

    if not email:
        flash("The confirmation link is invalid or has expired.")

    user = User.query.filter_by(email=email).first_or_404()

    if user.confirmed:
        flash("Account already confirmed. Please login.")
    else:
        user.confirmed = True
        user.email_confirmed_at = datetime.utcnow()
        db.session.add(user)
        db.session.commit()
        flash("You have confirmed your account.")
    return redirect(url_for("main.profile"))


@bp.route("/unconfirmed", methods=["GET"])
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for("main.profile"))
    flash("Please confirm your account!")
    return render_template("unconfirmed.html")


@bp.route("/resend")
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    send_email(
        redirect="auth.confirm_email",
        html="activate.html",
        recipients=current_user.email,
        subject="Please confirm your email",
        token=token
    )
    flash("A new confirmation email has been sent.")
    return redirect(url_for("auth.unconfirmed"))


@bp.route("/reset", methods=["GET", "POST"])
def reset():
    form = EmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        token = generate_confirmation_token(user.email)
        send_email(
            redirect="auth.reset_with_token",
            html="recover.html",
            recipients=user.email,
            subject="Password reset requested",
            token=token
        )
        flash("Check your email.")
        return redirect(url_for("auth.login"))
    return render_template("login.html")


@bp.route("/reset/<token>", methods=["GET", "POST"])
def reset_with_token(token):
    email = confirm_token(token)
    if not email:
        flash("The confirmation link is invalid or has expired.")
        return render_template("login.html")

    form = ResetPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first_or_404()

        user.password = form.password.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("auth.login"))

    return render_template("reset_with_token.html", form=form, token=token)
