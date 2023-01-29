from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS, cross_origin
from flask.helpers import send_from_directory
from werkzeug.utils import secure_filename
import os

import front_end_api_controller
import external_api_controller

app = Flask(__name__, static_folder = '../frontend/build/', static_url_path = '/')

app.register_blueprint(front_end_api_controller.bp)
app.register_blueprint(external_api_controller.bp)

CORS(app)

ALLOWED_EXTENSIONS = set(['csv', 'xlsx'])

#for production
ADMIN_PASS = os.environ['ADMIN_PASS']

#for local testing
#ADMIN_PASS = ''

def allowed_file(filename):
    return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def password_form():
    return '''<form method="post">
            <label for="pass">Please enter admin password:</label>
            <input type="password" id="pwd" name="pwd" required>
            <input type="submit" value="Sign in">
            </form>'''

def check_password(pwd):
    return pwd == ADMIN_PASS

@app.route("/testUpload")
@cross_origin()
def test_upload():
    return send_from_directory("./data/salary", "annual_aqi_by_county_2022.csv")

@app.route("/")
@cross_origin()
def serve_main():
    return send_from_directory(app.static_folder, 'index.html')

# TODO delete this
@app.route("/test", methods=['GET'])
@cross_origin()
def numbers():
    return {"numbers": ["four", "five"]}

@app.route("/admin", methods=['GET', 'POST'])
@cross_origin()
def serve_admin():
    if request.method == 'POST':
        pwd = request.form['pwd']
        if check_password(pwd):
            return send_from_directory('../frontend/', 'adminPage.html')
        else:
            return password_form()
    if request.method == 'GET':
        return password_form()
    


@app.route('/uploadSalary', methods = ['POST'])
@cross_origin()
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