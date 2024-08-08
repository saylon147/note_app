import logging
import os

from flask import Flask, current_app
from utils.extensions import init_db, bcrypt, jwt
from routes.auth import auth
from routes.notes import notes


def create_app():
    app = Flask(__name__)
    app.logger.setLevel(logging.DEBUG)
    app.config.from_object('config.Config')
    app.secret_key = "04f69912a0fd7dd7eb0a77954c76573cb71017cc4e179b1ce9ebedac5c1f07f8"

    # print(app.config)

    # 初始化扩展
    init_db(app.config["MONGO_URI"])
    bcrypt.init_app(app)
    jwt.init_app(app)

    # 注册蓝图
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(notes, url_prefix="/api")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
