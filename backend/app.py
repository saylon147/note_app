from flask import Flask
from utils.extensions import init_db, bcrypt, jwt
from routes.auth import auth
from routes.notes import notes


def create_app():
    app = Flask(__name__)
    app.config.from_object('utils.config.Config')

    # 初始化扩展
    init_db()
    bcrypt.init_app(app)
    jwt.init_app(app)

    # 注册蓝图
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(notes, url_prefix="/api")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
