from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import mongoengine as me


bcrypt = Bcrypt()
jwt = JWTManager()


# 初始化 MongoDB 连接
def init_db(host):
    me.connect(host=host)
