from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from models import db, BlogPost, Author

admin = Admin(name='Gents Edit Admin', template_mode='bootstrap4')

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

admin.add_view(SecureModelView(BlogPost, db.session))
admin.add_view(SecureModelView(Author, db.session))