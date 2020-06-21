import click

from datetime import datetime

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from application.app import db
from application.models import User, Role
from wsgi import app

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command("db", MigrateCommand)


@manager.command
def create_user():
    email = click.prompt("Email")
    username = click.prompt("Username")
    password = click.prompt("Password", hide_input=True, confirmation_prompt=True)
    role = click.prompt("Role")

    try:
        user = User(
            email=email,
            username=username,
            password=password,
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
