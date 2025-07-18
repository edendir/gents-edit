class Config:
    SECRET_KEY = '...'
    SESSION_TYPE = 'filesystem'
    MAIL_SERVER = 'smtp.example.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'user@example.com'
    MAIL_PASSWORD = 'password'
    FLASK_ADMIN_SWATCH = 'journal'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///blog.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_PERMANENT = False