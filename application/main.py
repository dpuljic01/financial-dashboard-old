from flask import Blueprint, render_template
from flask_login import login_required, current_user
from application.decorators import check_confirmed

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    if not current_user.is_authenticated:
        return render_template("login.html")
    return render_template("index.html")


@bp.route("/profile")
@login_required
@check_confirmed
def profile():
    return render_template("profile.html", user=current_user.first_name)
