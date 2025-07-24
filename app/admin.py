from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from app.models import db, BlogPost, Author, Image
from flask import redirect, url_for
from wtforms_sqlalchemy.fields import QuerySelectField

class SecureAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated or not current_user.is_admin:
            return redirect(url_for('auth.login'))
        return super().index()

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

class BlogPostAdmin(SecureModelView):
    pass  # Add customizations later if needed

class AuthorAdmin(SecureModelView):
    pass

class ImageAdmin(SecureModelView):
    form_overrides = {
        'blog_post': QuerySelectField
    }
    form_args = {
        'blog_post': {
            'query_factory': lambda: BlogPost.query.all(),
            'get_label': 'title'
        }
    }
    form_columns = ['filename', 'url', 'blog_post']

admin = Admin(name='Admin Panel', template_mode='bootstrap4', index_view=SecureAdminIndexView())

admin.add_view(SecureModelView(BlogPost, db.session))
admin.add_view(SecureModelView(Author, db.session))
admin.add_view(ImageAdmin(Image, db.session))