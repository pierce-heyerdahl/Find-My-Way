from flask import Flask, jsonify, request, redirect, url_for 
import flask_login
from flask_login import LoginManager, UserMixin
from flask_cors import CORS, cross_origin
from flask.helpers import send_from_directory
from werkzeug.utils import secure_filename
import os
from models import * 
from state_to_abreviation import abbrevStates
import pandas as pd
from dotenv import load_dotenv

import front_end_api_controller
import db_admin_upload_api

app = Flask(__name__, static_folder = '../frontend/build/', static_url_path = '/')

load_dotenv()

#for production
SECRET_KEY = os.environ['SECRET_KEY']

app.secret_key = SECRET_KEY

login_manager = LoginManager()

app.register_blueprint(front_end_api_controller.bp)
app.register_blueprint(db_admin_upload_api.bp)

login_manager.init_app(app)
CORS(app)

#Initializing DB and Schema

#production DB
DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_URL= DATABASE_URL[:8]+'ql' + DATABASE_URL[8:]

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db.init_app(app)

with app.app_context():
    db.create_all()
    
ALLOWED_EXTENSIONS = set(['csv', 'xlsx'])

#for production
ADMIN_PASS = os.environ['ADMIN_PASS']

#for local testing
#ADMIN_PASS = 'abc'

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

ALLOWED_EXTENSIONS = set(['csv', 'xlsx'])

def allowed_file(filename):
    return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# TODO delete this
def password_form():
    return '''<form method="post">
            <label for="pass">Please enter admin password:</label>
            <input type="password" id="pwd" name="pwd" required>
            <input type="submit" value="Sign in">
            </form>'''

@app.route("/")
@cross_origin()
def serve_main():
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/adminLogin", methods=['GET', 'POST'])
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
            return redirect(url_for('serve_admin'))
    return send_from_directory('../frontend/', 'adminLogin.html')

@app.route('/logout')
@cross_origin()
def logout():
  flask_login.logout_user()

  return redirect("/")

@app.errorhandler(404)
@cross_origin()
def not_found(e):
    return send_from_directory(app.static_folder, 'index.html')