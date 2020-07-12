from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user
from application.decorators import check_confirmed


bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/dash1")
@login_required
@check_confirmed
def dash1():
    return redirect("/dash1", code=302)


@bp.route("/dash2")
@login_required
@check_confirmed
def dash2():
    return redirect("/dash2", code=302)


@bp.route("/profile")
@login_required
@check_confirmed
def profile():
    return render_template("profile.html", user=current_user.first_name)
