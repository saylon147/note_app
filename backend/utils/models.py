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
    user = me.ReferenceField(User, required=True, reverse_delete_rule=me.CASCADE)   # User删除的时候Note一起删
    title = me.StringField(required=True)
    created_at = me.DateTimeField(default=datetime.now(timezone.utc))
    updated_at = me.DateTimeField(default=datetime.now(timezone.utc))
    tags = me.ListField(me.StringField(max_length=10), default=list)

    meta = {
        'indexes': [
            'tags',  # 为tags字段创建索引，以便进行筛选查询
        ],
        'allow_inheritance': True
    }


class TextNote(Note):
    content = me.StringField(required=True)
