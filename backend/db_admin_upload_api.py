from flask import Blueprint, jsonify, request, redirect, url_for, stream_with_context, Response, current_app, make_response, send_from_directory
from flask_login import login_required
import pandas as pd
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os
from models import *
from state_to_abreviation import abbrevStates


bp = Blueprint('db_admin_upload_api', __name__)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['csv', 'xlsx'])
    return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/adminPage')
@cross_origin()
@login_required
def adminPage():
    response = make_response(send_from_directory('../frontend/', 'adminPage.html'))
    response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return response

@bp.route('/uploadGeo', methods = ['POST'])
@cross_origin()
@login_required
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


            return (Response(parse_and_upload_geo_data_to_db(filename)))
        elif not file: return ("Please select a file to upload.")
    return ("Failure uploading file.")


def geo_data_to_db(geo_df: pd.DataFrame):
        with current_app.app_context():
            if(geo_df.empty):
                return("Error parsing file")
            try:
                yield('removing previous data...\n')
                num_rows_deleted = db.session.query(City).delete()
                yield(f'{num_rows_deleted} rows removed.<br>Uploading new data...')
                db.session.commit()
            except:
                db.session.rollback()
                yield("Failure uploading data.")
                return
            geo_df.to_sql('city', db.engine, if_exists='append', index_label='id')
        yield '<br>Data&#10 upload Successful.'


@stream_with_context
def parse_and_upload_geo_data_to_db(filename: str):
    yield('File upload successful, parsing...<br>')
    try:
        data = pd.read_excel(os.path.join('./data/geo', filename))
        # Abstract data that meet the criteria.
        USdata = data[(data['country'] == 'United States')]
        USdata.head()
        # Select columns we need and rename columns.
        data = pd.DataFrame(USdata, columns = ['city', 'admin_name', 'lat', 'lng'])
        data.rename(columns = {'city':'name', 'admin_name':'state'}, inplace=True)
        #add state abbreviation column
        data['abbr'] = data['state'].replace(abbrevStates)
    except pd.errors.EmptyDataError:
        yield("File is empty or has no data.")
        return
    except FileNotFoundError:
        yield("File not found.")
        return
    except pd.errors.ParserError:
        yield("File is not in the expected format.")
        return

    yield from geo_data_to_db(data)

@bp.route('/uploadCoL', methods = ['POST'])
@cross_origin()
@login_required
def upload_CoL():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):

            #make directory if it dosn't exist
            try:
                os.makedirs("./data/col")
            except OSError:
                pass # already exists

            filename = secure_filename(file.filename)
            file.save(os.path.join("./data/col", filename))
            
            return (Response(parse_col_to_db(filename)))
        elif not file: return 'Please select a file to upload.'
    return ("Failure uploading file.")

@stream_with_context
def parse_col_to_db(filename:str):
    yield 'File upload successful, parsing...\n'
    data = pd.DataFrame()
    stateAve = pd.DataFrame()
    try:
        data = pd.read_excel(os.path.join('./data/col', filename), sheet_name='Section 2 Index')
        yield 'dataframe created, parsing...\n'

        data = data.drop([0,1,2,3])
        yield 'drop unused columns, parsing...\n'

        data.rename(columns = {'Unnamed: 1':'STATE', '2022 Annual Average Section 2 Index':'URBAN AREA AND STATE', 'Unnamed: 4':'COMPOSITE INDEX'}, inplace = True)
        yield 'rename columns, parsing...\n'

        data = pd.DataFrame(data, columns = ['STATE','URBAN AREA AND STATE','COMPOSITE INDEX'])
        data['abbr'] = data['STATE'].replace(abbrevStates)
        yield 'create column for abreviations, parsing...\n'

        data['URBAN AREA AND STATE'] = data['URBAN AREA AND STATE'].str[:-3]
        yield 'remove abreviations from state column, parsing...\n'

        data.rename(columns = {'URBAN AREA AND STATE':'city', 'STATE':'state', 'COMPOSITE INDEX': 'coli'}, inplace=True)
        data = data.assign(city = data.city.str.split("-"))
        data = data.explode('city')
        yield 'split columns with multiple cities into seperate rows, parsing...\n'

        data = data[['city','state','coli']]
        data.reset_index(drop = True, inplace = True)
        yield 'resetting indices for db insertion, parsing...\n'
        
        stateAve = data.groupby(['state'])['coli'].mean().round(2).reset_index()
        yield 'create a table of state average indicies.\nParsing Complete.'
        
    except pd.errors.EmptyDataError:
        yield "File is empty or has no data.\n"
        return 
    except FileNotFoundError:
        yield "File not found.\n"
        return
    except pd.errors.ParserError:
        yield "File is not in the expected format.\n"
        return
    
    with current_app.app_context():

        if(data.empty or stateAve.empty):
            yield data.head().to_html()
            yield("Error parsing file\n")
            return

        #remove previous data since pandas to_sql doesn't support 
        try:
            yield 'removing previous data...\n'
            num_rows_deleted = db.session.query(CityCol).delete()
            num_state_rows_deleted = db.session.query(StateCol).delete()
            yield f'{num_rows_deleted} rows removed...\n'
            db.session.commit()
        except:
            db.session.rollback()
            yield ("Failure")
            return

        try:
            yield 'uploading city cost of living data...\n'
            data.to_sql('city_col', db.engine, if_exists='append', index_label='id')
            yield 'uploading state average cost of living data...\n'
            stateAve.to_sql('state_col', db.engine, if_exists='append', index_label='id')
        except:
            yield 'Failure, upload aborted.'
            return

    yield 'Success.'

# @bp.route('/uploadSalary', methods = ['POST'])
# @cross_origin()
# @login_required
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