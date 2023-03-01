from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS, cross_origin
from flask.helpers import send_from_directory
from werkzeug.utils import secure_filename
import os
from models import * 
from state_to_abreviation import abbrevStates
import pandas as pd

import front_end_api_controller

app = Flask(__name__, static_folder = '../frontend/build/', static_url_path = '/')

app.register_blueprint(front_end_api_controller.bp)

CORS(app)

#Initializing DB and Schema

#production DB
DATABASE_URL = os.environ['DATABASE_URL']
#registrationkey = os.environ['REGISTRATION_KEY']

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db.init_app(app)

with app.app_context():
    db.create_all()
    
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

# TODO delete this
@app.route("/testUpload")
@cross_origin()
def test_upload():
    return send_from_directory("./data/salary", "annual_aqi_by_county_2022.csv")

@app.route("/")
@cross_origin()
def serve_main():
    return send_from_directory(app.static_folder, 'index.html')

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
            
            #make directory if it dosn't exist
            try:
                os.makedirs("./data/salary")
            except OSError:
                pass # already exists
            
            file.save(os.path.join("./data/salary", filename))
            salaries = parse_salary_excel_file_to_df(filename)
            if(salaries.empty):
                return("Error parsing file")
            try:
                num_rows_deleted = db.session.query(Salary).delete()
                db.session.commit()
            except:
                db.session.rollback()
                return("Failure")
            
            try:
                salaries.to_sql('salary', db.engine, if_exists='append', index_label='id')
            except:
                return("Failure")
            
            return ("Success")
    return ("Failure")

@app.route('/uploadGeo', methods = ['POST'])
@cross_origin()
def upload_geo():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            #make the directory if it doesn't exist
            try:
                os.makedirs("./data/geo")
            except OSError:
                pass # already exists

            file.save(os.path.join("./data/geo", filename))

            geo = parse_geo_excel_file_to_df(filename)
            if(geo.empty):
                return("Error parsing file")
            try:
                num_rows_deleted = db.session.query(City).delete()
                db.session.commit()
            except:
                db.session.rollback()
                return("Failure")
            geo.to_sql('city', db.engine, if_exists='append', index_label='id')
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

def parse_salary_excel_file_to_df(filename) -> pd.DataFrame:
    try:
        data = pd.read_excel(os.path.join('./data/salary', filename))
        # Select columns we need, and replace symbols to 0.
        temp_data = pd.DataFrame(data, columns=['AREA_TITLE', 'PRIM_STATE', 'OCC_TITLE', 'H_MEAN', 'A_MEAN'])
        temp_data.replace('*', 0, inplace = True)
        temp_data.replace('#', 0, inplace = True)

        # Calculate Annual mean wage using Mean hourly wage that columns only have Hourly mean wage.
        temp_data.loc[(temp_data['H_MEAN'] != 0) & (temp_data['A_MEAN'] == 0), 'A_MEAN'] = (temp_data['H_MEAN'] * 1920).round(0)

        # Drop columns neither Hourly mean wage nor Annual mean wage.
        # Modify city names without State names.
        temp_data = temp_data[(temp_data['H_MEAN'] != 0) & (temp_data['A_MEAN'] != 0)]
        temp_data['AREA_TITLE'] = temp_data['AREA_TITLE'].apply(lambda x: x.split(',')[0])

        # Rename columns.
        final_data = pd.DataFrame(temp_data, columns = ['AREA_TITLE', 'PRIM_STATE', 'OCC_TITLE', 'A_MEAN'])
        final_data.rename(columns = {'AREA_TITLE':'city', 'PRIM_STATE':'abbr', 'OCC_TITLE':'job', 'A_MEAN':'salary'}, inplace = True)
        
        # Manipulate city names to divide the columns.
        final_data['city'] = final_data['city'].apply(lambda x: x.replace("--",","))
        final_data['city'] = final_data['city'].apply(lambda x: x.replace("-",","))

        # Divide columns by city name to refine the dataset.
        final_data = final_data.assign(city = final_data.city.str.split(","))
        final_data = final_data.explode('city')
        final_data.head()

        statesList = dict(zip(abbrevStates.values(), abbrevStates.keys()))
        final_data['state'] = final_data['abbr'].replace(statesList)
        final_data = final_data[['city','state','abbr','job', 'salary']]
        final_data.reset_index(drop=True, inplace=True)

        return final_data
    except pd.errors.EmptyDataError:
        print("File is empty or has no data.")
    except FileNotFoundError:
        print("File not found.")
    except pd.errors.ParserError:
        print("File is not in the expected format.")

    return pd.DataFrame()

def parse_geo_excel_file_to_df(filename) -> pd.DataFrame():
    try:
        data = pd.read_excel(os.path.join('./data/geo', filename))
        # Abstract data that meet the criteria.
        USdata = data[(data['country'] == 'United States')]
        USdata.head()
        # Select columns we need and rename columns.
        finalData = pd.DataFrame(USdata, columns = ['city', 'admin_name', 'lat', 'lng'])
        finalData.rename(columns = {'city':'name', 'admin_name':'state'}, inplace=True)
        #add state abbreviation column
        finalData['abbr'] = finalData['state'].replace(abbrevStates)
        return finalData
    except pd.errors.EmptyDataError:
        print("File is empty or has no data.")
    except FileNotFoundError:
        print("File not found.")
    except pd.errors.ParserError:
        print("File is not in the expected format.")

    return pd.DataFrame()
    
if __name__ == "__main__":
    #app.run(host = "0.0.0.0", debug = True, port = int(os.environ.get("PORT", 5000)))
    app.run()