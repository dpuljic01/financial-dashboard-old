import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.getenv("APP_SETTINGS"))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

from application.models import User


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/<name>")
def hello_name(name):
    return "Hello {}!".format(name)


if __name__ == "__main__":
    app.run()
