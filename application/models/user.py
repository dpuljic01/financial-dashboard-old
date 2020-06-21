from uuid import uuid4

import safe
from flask_login import UserMixin
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates
from sqlalchemy_utils import PasswordType

from application.app import db
from application.helpers.errors import InvalidValueError
from application.models.mixin import TimestampMixin


def get_uuid():
    return str(uuid4())


class User(db.Model, UserMixin, TimestampMixin):
    """
    User model.
    `account_type`: `basic` and `premium`, also `admin`, but not sure about that yet. It"s `basic` by default
    `status`: by default inactive, becomes active after email confirmation
    """
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    email = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(PasswordType(schemes=["bcrypt"]), nullable=False)
    active = db.Column("is_active", db.Boolean(), nullable=False, server_default="1")
    email_confirmed_at = db.Column(db.DateTime())

    roles = db.relationship("Role", secondary="user_roles")

    __table_args__ = (
        UniqueConstraint(
            "email", "username",
            name="uq_users_email_username",
        ),
    )

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    @property
    def json(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "account_type": self.account_type,
            "status": self.status,
        }

    @validates("password")
    def validate_password(self, key, password):
        strength = safe.check(password, level=safe.MEDIUM)
        if not strength.valid:
            raise InvalidValueError(message=strength.message)
        return password

    @staticmethod
    def auth(username, password, active=True):
        user = User.query.filter_by(username=username, active=active).first()
        if user:
            return user.password == password
        return False

    def __repr__(self):
        return f"User(id={self.id}, email={self.email}, account_type={self.account_type}, status={self.status})"


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


class UserRoles(db.Model):
    __tablename__ = "user_roles"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id", ondelete="CASCADE"))
    role_id = db.Column(db.Integer(), db.ForeignKey("roles.id", ondelete="CASCADE"))

