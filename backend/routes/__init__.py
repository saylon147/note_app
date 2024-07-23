from flask import Blueprint

# Importing blueprints
from .auth import auth_bp
from .notes import notes_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(notes_bp, url_prefix='/api/notes')
