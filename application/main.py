from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user
from application.decorators import check_confirmed

bp = Blueprint("main", __name__)


@bp.route("/")
@login_required
@check_confirmed
def index():
    return render_template("index.html")


@bp.route("/dashboard")
@login_required
@check_confirmed
def dashboard():
    return redirect("/dashboard", code=302)


@bp.route("/profile")
@login_required
@check_confirmed
def profile():
    return render_template("profile.html", user=current_user.first_name)
