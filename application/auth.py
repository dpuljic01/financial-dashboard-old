from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required

from application.app import db
from application.email import send_email
from application.models import User
from application.token import generate_confirmation_token, confirm_token

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.auth(email=email, password=password)

    if not user:
        flash("Please check your login details and try again.")
        return redirect(url_for("auth.login"))

    login_user(user=user, remember=remember)
    return redirect(url_for("main.profile"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("login.html")

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if user:
        flash("Email address already exists")
        return redirect(url_for("auth.register"))

    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
    }
    user = User(**payload)

    # add the new user to the database
    db.session.add(user)
    db.session.commit()

    token = generate_confirmation_token(user.email)
    send_email(recipients=user.email, token=token)

    login_user(user)
    flash("A confirmation email has been sent via email.", "success")

    return redirect(url_for("auth.unconfirmed"))


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@bp.route("/confirm/<string:token>")
@login_required
def confirm_email(token):
    email = confirm_token(token)

    if not email:
        flash("The confirmation link is invalid or has expired.", "danger")

    user = User.query.filter_by(email=email).first_or_404()

    if user.confirmed:
        flash("Account already confirmed. Please login.", "success")
    else:
        user.confirmed = True
        user.email_confirmed_at = datetime.utcnow()
        db.session.add(user)
        db.session.commit()
        flash("You have confirmed your account.", "success")
    return redirect(url_for("main.profile"))


@bp.route("/unconfirmed", methods=["GET"])
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for("main.profile"))
    flash("Please confirm your account!", "warning")
    return render_template("unconfirmed.html")
