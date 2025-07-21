from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    tags = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    author = db.Relationship('Author', back_populates='blog_posts')
    images = db.relationship('Image', backref='blog_post', lazy=True)
    
class Author(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bio = db.Column(db.Text, nullable=True)
    profile_image_url = db.Column(db.String(200), nullable=True)
    user = db.relationship('User', backref='author', uselist=False, lazy=True)
    blog_posts = db.relationship('BlogPost', back_populates='author', lazy='dynamic')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime, default=db.func.current_timestamp())
    author_profile = db.relationship('Author', backref='user', uselist=False, lazy=True)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    blog_post_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'), nullable=False)
    blog_post = db.relationship('BlogPost', back_populates='images')
