import flask_login
from flask import Blueprint, request, redirect, url_for, send_from_directory
from flask_cors import cross_origin
from flask_login import LoginManager, UserMixin
import os


bp = Blueprint('auth_bp', __name__)

login_manager = LoginManager()

ADMIN_PASS = os.environ['ADMIN_PASS']
users = {'admin':{'pw':ADMIN_PASS}}

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return
    
    user = User()
    user.id = username
    return user

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if username not in users:
        return
    
    user = User()
    user.id = username

    user.is_authenticated = request.form['pw'] == users[username]['pw']

    return user

@bp.route("/adminLogin", methods=['GET', 'POST'])
@cross_origin()
def serve_admin():
    if request.method == 'POST':
        username = request.form.get('username')
        if username not in users:
            return redirect(url_for('serve_admin'))
        if request.form.get('pw') == users[username]['pw']:
            user = User()
            user.id = username
            flask_login.login_user(user)
            return redirect('/adminPage')
        else:
            return redirect('/adminLogin')
    return send_from_directory('../frontend/', 'adminLogin.html')

@bp.route('/logout')
@cross_origin()
def logout():
    flask_login.logout_user()
    return redirect("/")
