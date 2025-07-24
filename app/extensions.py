from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_session import Session
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
mail = Mail()
session_manager = Session()
login_manager = LoginManager()
migrate = Migrate()