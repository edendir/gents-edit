import os
from dotenv import load_dotenv
from pathlib import Path

# Load from .env
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

base_dir = Path(__file__).resolve().parent.parent

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-key')
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    SESSION_TYPE = 'filesystem'
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    PREFERRED_URL_SCHEME = 'https'
    RECPATCHA_SITE_KEY = os.getenv('RECAPTCHA_SITE_KEY')
    RECPATCHA_SECRET_KEY = os.getenv('RECAPTCHA_SECRET_KEY')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL')
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('PRODUCTION_DATABASE_URL')