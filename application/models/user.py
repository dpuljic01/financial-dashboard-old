from uuid import uuid4

from sqlalchemy.dialects.postgresql import JSONB, ENUM, UUID

from app import db
from application.models.mixin import TimestampMixin


def get_uuid():
    return str(uuid4())


class User(db.Model, TimestampMixin):
    """
    User model.
    `account_type`: `basic` and `premium`, also `admin`, but not sure about that yet. It's `basic` by default
    `status`: by default inactive, becomes active after email confirmation
    """
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    email = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    account_type = db.Column(ENUM("basic", "premium", "admin", create_type=False), nullable=False, default="basic")
    status = db.Column(ENUM("active", "inactive", create_type=False), nullable=False, default="inactive")

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

    def __repr__(self):
        return f"User(id={self.id}, email={self.email}, account_type={self.account_type}, status={self.status})"

