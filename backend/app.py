from flask import Flask
from config import Config
from extensions import bcrypt, jwt, mongo


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    bcrypt.init_app(app)
    jwt.init_app(app)
    mongo.init_app(app)

    from routes.auth import auth_bp
    from routes.notes import notes_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(notes_bp, url_prefix='/api/notes')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
