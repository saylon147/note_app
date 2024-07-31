import mongoengine as me
from datetime import datetime, timezone
from .extensions import bcrypt


class User(me.Document):
    username = me.StringField(required=True, unique=True)
    password = me.StringField(required=True)
    registered_at = me.DateTimeField(default=datetime.now(timezone.utc))

    def verify_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password, password)


class Note(me.Document):
    user = me.ReferenceField(User, required=True)
    title = me.StringField(required=True)
    content = me.StringField(required=True)
    created_at = me.DateTimeField(default=datetime.now(timezone.utc))
    updated_at = me.DateTimeField(default=datetime.now(timezone.utc))
