import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import db, BlogPost, Author, User
from datetime import datetime

app = create_app()
app.app_context().push()
admin = User.query.filter_by(username='robbie').first()

if not admin:
    print("Admin user not found. Please create the admin first.")
    exit()

# Define post data here or dynamically
post = BlogPost(
    title="New Post Title",
    content="This is the content of the new post.",
    tags="flask,admin,test",
    author_id=admin.id,
    created_at=datetime.utcnow()
)

db.session.add(post)
db.session.commit()

print(f"Post '{post.title}' created successfully.")