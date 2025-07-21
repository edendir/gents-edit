import pytest
from app.models import BlogPost, Author, User, db

# Helper functions
def create_user_and_author():
    user = User(username="testuser", password_hash="hashedpass")
    db.session.add(user)
    db.session.flush()  # Ensures user.id is assigned

    author = Author(id=user.id, name="Test Author", email="test@example.com")
    db.session.add(author)
    db.session.commit()
    return author

def create_blog_post():
    author = create_user_and_author()
    post = BlogPost(
        title="Test Post",
        content="This is test content.",
        author_id=author.id,
        tags="style,test"
    )
    db.session.add(post)
    db.session.commit()
    return post

# CRUD Tests

def test_create_blog_post(app):
    with app.app_context():
        post = create_blog_post()
        assert post.id is not None
        assert BlogPost.query.count() == 1

def test_read_blog_post(app):
    with app.app_context():
        create_blog_post()
        post = BlogPost.query.first()
        assert post is not None
        assert post.title == "Test Post"

def test_update_blog_post(app):
    with app.app_context():
        post = create_blog_post()
        post.title = "Updated Title"
        db.session.commit()

        updated = BlogPost.query.first()
        assert updated.title == "Updated Title"

def test_delete_blog_post(app):
    with app.app_context():
        post = create_blog_post()
        db.session.delete(post)
        db.session.commit()

        assert BlogPost.query.count() == 0
