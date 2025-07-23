import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import db, User

def create_admin():
    app = create_app()
    with app.app_context():
        username = input("Enter admin username: ").strip()
        password = input("Enter admin password: ").strip()

        # Check if username already exists
        existing = User.query.filter_by(username=username).first()
        if existing:
            print(f"User '{username}' already exists.")
            return

        admin_user = User(username=username, is_admin=True)
        admin_user.set_password(password)
        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin user '{username}' created successfully.")

if __name__ == '__main__':
    create_admin()
