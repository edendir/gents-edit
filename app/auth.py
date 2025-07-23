from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from app.models import User

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin.index'))
        else:
            flash('Invalid credentials')
    else:
        return render_template('login.html')

@auth_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
