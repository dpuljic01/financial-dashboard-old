from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required

from application.app import db
from application.email import send_email
from application.models import User
from application.token import generate_confirmation_token, confirm_token

bp = Blueprint("auth", __name__)


@bp.route("/login")
def login():
    return render_template("login.html")


@bp.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.auth(username=username, password=password)

    if not user:
        flash("Please check your login details and try again.")
        return redirect(url_for("auth.login"))

    login_user(user=user, remember=remember)
    return redirect(url_for("main.profile"))


@bp.route("/signup", methods=["GET"])
def signup():
    return render_template("signup.html")


@bp.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash("Email address already exists")
        return redirect(url_for("auth.signup"))

    # create new user with the form data. Hash the password so plaintext version isn"t saved.
    payload = {
        "email": email,
        "username": username,
        "password": password,
        "confirmed": False
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
        user.confirmed_on = datetime.utcnow()
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
