import os
from flask import Flask
from app.config import Config, ProductionConfig, DevelopmentConfig

def create_app():
    app = Flask(__name__)

    print("Creating Flask app with configuration...")

    from app.extensions import db, mail, session_manager, login_manager, migrate
    from app.admin import admin
    from app.auth import auth_blueprint
    from app.routes import main
    from app.models import User

    config_class = ProductionConfig if os.getenv('FLASK_ENV') == 'production' else DevelopmentConfig
    app.config.from_object(config_class)
    print(f"Using configuration: {config_class.__name__}")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://neondb_owner:npg_VkC3mwE9FGjf@ep-noisy-math-ae4kjfyv-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require'  # Placeholder to ensure it's set
    print("using database URI:", app.config['SQLALCHEMY_DATABASE_URI'])
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