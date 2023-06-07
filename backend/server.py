from flask import Flask
from flask_cors import CORS, cross_origin
from flask.helpers import send_from_directory
import os
from backend.models import * 
from dotenv import load_dotenv
load_dotenv()

from backend.front_end_api_controller import bp as frontend_api_bp
import backend.db_admin_upload_api as db_admin_upload_api
import backend.auth as auth

app = Flask(__name__, static_folder = '../frontend/build/', static_url_path = '/')

#sets a secret key variable for flask_login
SECRET_KEY = os.environ['SECRET_KEY']

app.secret_key = SECRET_KEY

#register blueprints
app.register_blueprint(frontend_api_bp)
app.register_blueprint(db_admin_upload_api.bp)
app.register_blueprint(auth.bp)

#initialize flask_login extension
auth.login_manager.init_app(app)
CORS(app)

#Initializing DB and Schema
DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_URL= DATABASE_URL[:8]+'ql' + DATABASE_URL[8:]

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
@cross_origin()
def serve_main():
    return send_from_directory(app.static_folder, 'index.html')

@app.errorhandler(404)
@cross_origin()
def not_found(e):
    return send_from_directory(app.static_folder, 'index.html')