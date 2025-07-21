from flask import Flask
from app.config import Config
from app.extensions import db, mail, session_manager
from app.admin import admin

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    session_manager.init_app(app)
    admin.init_app(app)

    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app