from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import mongoengine as me
from utils.config import Config


bcrypt = Bcrypt()
jwt = JWTManager()


# 初始化 MongoDB 连接
def init_db():
    me.connect(host=Config.MONGO_URI)
