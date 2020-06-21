import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager
from flask_babelex import Babel
from flask_mail import Mail

load_dotenv()

db = SQLAlchemy()
mail = Mail()
babel = Babel()

from application import auth, main

blueprints = (
    auth,
    main,
)


def create_app():
    app = Flask(__name__)

    app.config.from_object(os.getenv("APP_SETTINGS"))
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Initialize Flask-BabelEx

    mail.init_app(app)
    babel.init_app(app)

    from application.models import User

    user_manager = UserManager(app, db, User)
    user_manager.login_manager.login_view = "auth.login"

    @user_manager.login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    register_blueprints(app)
    return app


def register_blueprints(app):
    for blueprint in blueprints:
        app.register_blueprint(blueprint.bp)
