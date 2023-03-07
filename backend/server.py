from flask import Flask, jsonify, request, redirect, url_for, make_response
import flask_login
from flask_login import LoginManager, UserMixin
from flask_cors import CORS, cross_origin
from flask.helpers import send_from_directory
from werkzeug.utils import secure_filename
import os

import front_end_api_controller
import external_api_controller

app = Flask(__name__, static_folder = '../frontend/build/', static_url_path = '/')

#for production
SECRET_KEY = os.environ['SECRET_KEY']

#for local testing
#SECRET_KEY = 'key1'

app.secret_key = SECRET_KEY

login_manager = LoginManager()

app.register_blueprint(front_end_api_controller.bp)
app.register_blueprint(external_api_controller.bp)

login_manager.init_app(app)
CORS(app)

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

# TODO delete this
def check_password(pwd):
    return pwd == ADMIN_PASS

# TODO delete this
@app.route("/testUpload")
@cross_origin()
def test_upload():
    return send_from_directory("./data/salary", "annual_aqi_by_county_2022.csv")

@app.route("/")
@cross_origin()
def serve_main():
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/adminLogin", methods=['GET', 'POST'])
@cross_origin()
def serve_admin():
    if request.method == 'POST':
        username = request.form.get('username')
        if request.form.get('pw') == users[username]['pw']:
            user = User()
            user.id = username
            flask_login.login_user(user)
            return redirect(url_for('adminPage'))
    return send_from_directory('../frontend/', 'adminLogin.html')

@app.route('/adminPage')
@cross_origin()
@flask_login.login_required
def adminPage():
    response = make_response(send_from_directory('../frontend/', 'adminPage.html'))
    response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return response

@app.route('/logout')
@cross_origin()
def logout():
  flask_login.logout_user()

  return redirect("/")

@app.route('/uploadSalary', methods = ['POST'])
@cross_origin()
@flask_login.login_required
def upload_salary():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join("./data/salary", filename))
            return ("Success")
    return ("Failure")

@app.route('/uploadCoL', methods = ['POST'])
@cross_origin()
@flask_login.login_required
def upload_CoL():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join("./data/col", filename))
            return ("Success")
    return ("Failure")

@app.errorhandler(404)
@cross_origin()
def not_found(e):
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    #app.run(host = "0.0.0.0", debug = True, port = int(os.environ.get("PORT", 5000)))
    app.run()