import click

from datetime import datetime

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server

from application.extensions import db
from application.models import User, Role
from wsgi import app

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command("runserver", Server(host="0.0.0.0"))
manager.add_command("db", MigrateCommand)


@manager.command
def create_user():
    email = click.prompt("Email")
    first_name = click.prompt("First name")
    last_name = click.prompt("Last name")
    password = click.prompt("Password", hide_input=True, confirmation_prompt=True)
    role = click.prompt("Role")

    try:
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            confirmed=True,
            email_confirmed_at=datetime.utcnow()
        )
        role = Role(name=role)
        user.roles.append(role)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    manager.run()
