from flask import Flask
from app.config import Config
from app.extensions import db, mail, session_manager, login_manager, migrate
from app.admin import admin
from app.auth import auth_blueprint
from app.routes import main
from app.models import User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    session_manager.init_app(app)
    admin.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main)
    app.register_blueprint(auth_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    login_manager.login_view = 'auth.login'
    return app