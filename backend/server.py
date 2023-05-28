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

#for local testing
#SECRET_KEY = 'key1'

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

# @app.route('/uploadSalary', methods = ['POST'])
# @cross_origin()
# @flask_login.login_required
# def upload_salary():
#     if request.method == 'POST':
#         file = request.files['file']
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
            
#             #make directory if it dosn't exist
#             try:
#                 os.makedirs("./data/salary")
#             except OSError:
#                 pass # already exists
            
#             file.save(os.path.join("./data/salary", filename))
            
#             threading.Thread(target=salary_file_to_db, args=(filename,)).start()
            
#             return ("Successful upload, parsing and uploading to db...")
#     return ("Failure")

# def salary_file_to_db(filename:str):
#     salaries = parse_salary_excel_file_to_df(filename)
#     with app.app_context():
#         if(salaries.empty):
#             return("Error parsing file")
#         try:
#             num_rows_deleted = db.session.query(Salary).delete()
#             db.session.commit()
#         except:
#             db.session.rollback()
#             return("Failure")
        
#         try:
#             salaries.to_sql('salary', db.engine, if_exists='append', index_label='id')
#         except:
#             return("Failure")
#         return("Success")

@app.errorhandler(404)
@cross_origin()
def not_found(e):
    return send_from_directory(app.static_folder, 'index.html')

# def parse_salary_excel_file_to_df(filename) -> pd.DataFrame:
#     try:
#         data = pd.read_excel(os.path.join('./data/salary', filename))
#         # Select columns we need, and replace symbols to 0.
#         temp_data = pd.DataFrame(data, columns=['AREA_TITLE', 'PRIM_STATE', 'OCC_TITLE', 'H_MEAN', 'A_MEAN'])
#         temp_data.replace('*', 0, inplace = True)
#         temp_data.replace('#', 0, inplace = True)

#         # Calculate Annual mean wage using Mean hourly wage that columns only have Hourly mean wage.
#         temp_data.loc[(temp_data['H_MEAN'] != 0) & (temp_data['A_MEAN'] == 0), 'A_MEAN'] = (temp_data['H_MEAN'] * 1920).round(0)

#         # Drop columns neither Hourly mean wage nor Annual mean wage.
#         # Modify city names without State names.
#         temp_data = temp_data[(temp_data['H_MEAN'] != 0) & (temp_data['A_MEAN'] != 0)]
#         temp_data['AREA_TITLE'] = temp_data['AREA_TITLE'].apply(lambda x: x.split(',')[0])

#         # Rename columns.
#         final_data = pd.DataFrame(temp_data, columns = ['AREA_TITLE', 'PRIM_STATE', 'OCC_TITLE', 'A_MEAN'])
#         final_data.rename(columns = {'AREA_TITLE':'city', 'PRIM_STATE':'abbr', 'OCC_TITLE':'job', 'A_MEAN':'salary'}, inplace = True)
        
#         # Manipulate city names to divide the columns.
#         final_data['city'] = final_data['city'].apply(lambda x: x.replace("--",","))
#         final_data['city'] = final_data['city'].apply(lambda x: x.replace("-",","))

#         # Divide columns by city name to refine the dataset.
#         final_data = final_data.assign(city = final_data.city.str.split(","))
#         final_data = final_data.explode('city')
#         final_data.head()

#         statesList = dict(zip(abbrevStates.values(), abbrevStates.keys()))
#         final_data['state'] = final_data['abbr'].replace(statesList)
#         final_data = final_data[['city','state','abbr','job', 'salary']]
#         final_data.reset_index(drop=True, inplace=True)

#         return final_data
#     except pd.errors.EmptyDataError:
#         print("File is empty or has no data.")
#     except FileNotFoundError:
#         print("File not found.")
#     except pd.errors.ParserError:
#         print("File is not in the expected format.")

#     return pd.DataFrame()

# def parse_geo_excel_file_to_df(filename) -> pd.DataFrame():
#     try:
#         data = pd.read_excel(os.path.join('./data/geo', filename))
#         # Abstract data that meet the criteria.
#         USdata = data[(data['country'] == 'United States')]
#         USdata.head()
#         # Select columns we need and rename columns.
#         finalData = pd.DataFrame(USdata, columns = ['city', 'admin_name', 'lat', 'lng'])
#         finalData.rename(columns = {'city':'name', 'admin_name':'state'}, inplace=True)
#         #add state abbreviation column
#         finalData['abbr'] = finalData['state'].replace(abbrevStates)
#         return finalData
#     except pd.errors.EmptyDataError:
#         print("File is empty or has no data.")
#     except FileNotFoundError:
#         print("File not found.")
#     except pd.errors.ParserError:
#         print("File is not in the expected format.")
# 
    # return pd.DataFrame()