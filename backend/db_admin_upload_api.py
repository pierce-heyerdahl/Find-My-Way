from flask import Blueprint, request, stream_with_context, Response, current_app, make_response, send_from_directory
from flask_login import login_required
import pandas as pd
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
import os
from backend.models import *
from backend.state_to_abreviation import abbrevStates
from backend.front_end_api_controller import clear_cache


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

            clear_cache()

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
                return("Error parsing file<br>")
            try:
                yield('removing previous data...<br>')
                num_rows_deleted = db.session.query(City).delete()
                yield(f'{num_rows_deleted} rows removed.<br>Uploading new data...<br>')
                db.session.commit()
            except:
                db.session.rollback()
                yield("Failure uploading data.<br>")
                return
            geo_df.to_sql('city', db.engine, if_exists='append', index_label='id')
        yield 'Data upload Successful.<br>'


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

            clear_cache()

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
    yield 'File upload successful, parsing...<br>'
    data = pd.DataFrame()
    stateAve = pd.DataFrame()
    try:
        data = pd.read_excel(os.path.join('./data/col', filename), sheet_name='Section 2 Index')
        yield 'dataframe created, parsing...<br>'

        data = data.drop([0,1,2,3])
        yield 'drop unused columns, parsing...<br>'

        data.rename(columns = {'Unnamed: 1':'STATE', '2022 Annual Average Section 2 Index':'URBAN AREA AND STATE', 'Unnamed: 4':'COMPOSITE INDEX'}, inplace = True)
        yield 'rename columns, parsing...<br>'

        data = pd.DataFrame(data, columns = ['STATE','URBAN AREA AND STATE','COMPOSITE INDEX'])
        data['abbr'] = data['STATE'].replace(abbrevStates)
        yield 'create column for abreviations, parsing...<br>'

        data['URBAN AREA AND STATE'] = data['URBAN AREA AND STATE'].str[:-3]
        yield 'remove abreviations from state column, parsing...<br>'

        data.rename(columns = {'URBAN AREA AND STATE':'city', 'STATE':'state', 'COMPOSITE INDEX': 'coli'}, inplace=True)
        data = data.assign(city = data.city.str.split("-"))
        data = data.explode('city')
        yield 'split columns with multiple cities into seperate rows, parsing...<br>'

        data = data[['city','state','coli']]
        data.reset_index(drop = True, inplace = True)
        data.dropna(axis=0, inplace=True)
        yield 'resetting indices for db insertion, parsing...<br>'
        
        stateAve = data.groupby(['state'])['coli'].mean().round(2).reset_index()
        yield 'create a table of state average indicies.<br>Parsing Complete.<br>'
        
    except pd.errors.EmptyDataError:
        yield "File is empty or has no data.<br>"
        return 
    except FileNotFoundError:
        yield "File not found.<br>"
        return
    except pd.errors.ParserError:
        yield "File is not in the expected format.<br>"
        return
    
    with current_app.app_context():

        if(data.empty or stateAve.empty):
            yield data.head().to_html()
            yield("Error parsing file<br>")
            return
         
        #remove previous data since pandas to_sql doesn't support 
        try:
            yield 'removing previous data...<br>'
            num_rows_deleted = db.session.query(CityCol).delete()
            num_state_rows_deleted = db.session.query(StateCol).delete()
            yield f'{num_rows_deleted} city rows removed...<br>'
            yield f'{num_state_rows_deleted} state rows removed...<br>'
            db.session.commit()
        except:
            db.session.rollback()
            yield ("Failure")
            return

        try:
            yield 'uploading city cost of living data...<br>'
            data.to_sql('city_col', db.engine, if_exists='append', index_label='id')
            yield 'uploading state average cost of living data...<br>'
            stateAve.to_sql('state_col', db.engine, if_exists='append', index_label='id')
        except:
            yield 'Failure, upload aborted.'
            return

    yield 'Success.'

@bp.route('/uploadSalary', methods = ['POST'])
@cross_origin()
@login_required
def upload_salary():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            clear_cache()
            
            #make directory if it dosn't exist
            try:
                os.makedirs("./data/salary")
            except OSError:
                pass # already exists
            
            file.save(os.path.join("./data/salary", filename))
            
            return (Response(parse_salary_excel_file_upload_to_db(filename)))
    return ("Failure uploading file.")

def salary_file_to_db(salaries: pd.DataFrame):
    with current_app.app_context():
        if(salaries.empty):
            yield("Error parsing file")
            return
        try:
            
            num_rows_deleted = db.session.query(Salary).delete()
            db.session.commit()
            yield(f'Previous data ({num_rows_deleted} rows) removed, uploading new data...<br>')
        except:
            db.session.rollback()
            yield("Failure inserting into db...")
            return
        try:
            salaries.to_sql('salary', db.engine, if_exists='append', index_label='id')
        except:
            return("Failure")
        yield('DB upload complete.')
        return

@stream_with_context
def parse_salary_excel_file_upload_to_db(filename):
    yield "Successful upload, parsing and uploading to db...<br>"
    try:
        data = pd.read_excel(os.path.join('./data/salary', filename))
        # Select columns we need, and replace symbols to 0.
        yield 'Selecting columns, replace nan...<br>'
        temp_data = pd.DataFrame(data, columns=['AREA_TITLE', 'PRIM_STATE', 'OCC_TITLE', 'H_MEAN', 'A_MEAN'])
        temp_data.replace('*', 0, inplace = True)
        temp_data.replace('#', 0, inplace = True)

        # Calculate Annual mean wage using Mean hourly wage that columns only have Hourly mean wage.
        yield 'Calculating annual mean wages...<br>'
        temp_data.loc[(temp_data['H_MEAN'] != 0) & (temp_data['A_MEAN'] == 0), 'A_MEAN'] = (temp_data['H_MEAN'] * 1920).round(0)

        # Drop columns neither Hourly mean wage nor Annual mean wage.
        # Modify city names without State names.
        yield 'Drop rows with no wage data...<br>'
        temp_data = temp_data[(temp_data['H_MEAN'] != 0) & (temp_data['A_MEAN'] != 0)]
        temp_data['AREA_TITLE'] = temp_data['AREA_TITLE'].apply(lambda x: x.split(',')[0])

        # Rename columns.
        final_data = pd.DataFrame(temp_data, columns = ['AREA_TITLE', 'PRIM_STATE', 'OCC_TITLE', 'A_MEAN'])
        final_data.rename(columns = {'AREA_TITLE':'city', 'PRIM_STATE':'abbr', 'OCC_TITLE':'job', 'A_MEAN':'salary'}, inplace = True)
        
        # Manipulate city names to divide the columns.
        yield 'Separating rows for multiple cities...<br>'
        final_data['city'] = final_data['city'].apply(lambda x: x.replace("--",","))
        final_data['city'] = final_data['city'].apply(lambda x: x.replace("-",","))

        # Divide columns by city name to refine the dataset.
        final_data = final_data.assign(city = final_data.city.str.split(","))
        final_data = final_data.explode('city')

        statesList = dict(zip(abbrevStates.values(), abbrevStates.keys()))
        final_data['state'] = final_data['abbr'].replace(statesList)
        final_data = final_data[['city','state','abbr','job', 'salary']]
        final_data.reset_index(drop=True, inplace=True)

    except pd.errors.EmptyDataError:
        yield("File is empty or has no data.")
        return
    except FileNotFoundError:
        yield("File not found.")
        return
    except pd.errors.ParserError:
        yield("File is not in the expected format.")
        return

    yield 'Parsing complete uploading to DB...'
    yield from salary_file_to_db(final_data)
    return