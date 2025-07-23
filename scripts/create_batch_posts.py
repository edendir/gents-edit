import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.extensions import db
from app.models import User, BlogPost
from faker import Faker
from datetime import datetime, timedelta
import random

# Setup
app = create_app()
app.app_context().push()
fake = Faker()

# Ensure admin user exists
admin = User.query.filter_by(username='admin').first()
if not admin:
    print("Admin user not found. Please create the admin user first.")
    exit()

# Tag pool
tag_pool = ["flask", "webdev", "style", "tech", "blog", "python", "sqlalchemy"]

# Helper to get random date between 2020 and now
def random_date(start_year=2020):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime.now()
    delta = end_date - start_date
    return start_date + timedelta(days=random.randint(0, delta.days))

# Generate posts
posts = []
for _ in range(15):
    post = BlogPost(
        title=fake.sentence(nb_words=6),
        content=fake.paragraph(nb_sentences=10),
        tags=",".join(random.sample(tag_pool, k=random.randint(2, 4))),
        created_at=random_date(),
        author_id=admin.id
    )
    posts.append(post)

# Insert into DB
db.session.bulk_save_objects(posts)
db.session.commit()
print(f"{len(posts)} blog posts successfully created.")
