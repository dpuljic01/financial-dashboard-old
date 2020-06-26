import os

import dash
from dotenv import load_dotenv
from flask import Flask
from flask.helpers import get_root_path
from flask_login import login_required

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config.from_object(os.getenv("APP_SETTINGS"))
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # prepared for possibility of multiple dash apps, e.g. dash2
    from application.dash1.layout import layout
    from application.dash1.callbacks import register_callbacks
    register_dashapp(app, "Dashapp 1", "dashboard", layout, register_callbacks)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_dashapp(app, title, base_pathname, layout, register_callbacks_fun):
    # Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    my_dashapp = dash.Dash(
        __name__,
        server=app,
        url_base_pathname=f"/{base_pathname}/",
        assets_folder=f"{get_root_path(__name__)}/{base_pathname}/assets/",
        meta_tags=[meta_viewport]
    )

    with app.app_context():
        my_dashapp.title = title
        my_dashapp.layout = layout
        register_callbacks_fun(my_dashapp)
    _protect_dashviews(my_dashapp)


def _protect_dashviews(dashapp):
    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.config.url_base_pathname):
            dashapp.server.view_functions[view_func] = login_required(dashapp.server.view_functions[view_func])


def register_extensions(app):
    from application.extensions import db
    from application.extensions import login
    from application.extensions import migrate
    from application.extensions import mail
    from application.extensions import babel
    from application.extensions import csrf

    db.init_app(app)
    login.init_app(app)
    login.login_view = "auth.login"
    migrate.init_app(app, db)
    mail.init_app(app)
    babel.init_app(app)
    # csrf.init_app(app)


def register_blueprints(app):
    from application import auth, main

    blueprints = (
        auth,
        main,
    )

    for blueprint in blueprints:
        app.register_blueprint(blueprint.bp)
