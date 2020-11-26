import uuid
import datetime

from web import db

from flask_login import UserMixin

from sqlalchemy.types import CHAR
from sqlalchemy.types import TypeDecorator

from sqlalchemy.dialects.postgresql import UUID


class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    """

    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == "postgresql":
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value


class User(db.Model, UserMixin):
	id = db.Column(db.String, primary_key=True)
	id_type = db.Column(db.String(18), nullable=False)

	pfp = db.Column(db.String)
	name = db.Column(db.String(32), nullable=False)
	join_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
	
	projects = db.relationship("Project", backref="user", lazy=True)

	def __repr__(self):
		return f"<User @id:{self.id}, @name:{self.name}>"


class Project(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	language = db.Column(db.String, nullable=False)
	content = db.Column(db.String, nullable=False)

	user_id = db.Column(db.String, db.ForeignKey("user.id"), nullable=False)

	def __repr__(self):
		return f"<Project @user_id:{self.user_id}>"

