from flask import Blueprint
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import psycopg2
import os

bp = Blueprint('front_end_api_controller_bp', __name__)

#local DB
#load_dotenv()
#DATABASE = os.getenv('DATABASE')
#DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
#DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')

#production DB
DATABASE_URL = os.environ['DATABASE_URL']

def get_db_connection():
    try:
        #local DB
        #conn = psycopg2.connect(database = DATABASE, user = DATABASE_USERNAME, password = DATABASE_PASSWORD)

        #production DB
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except:
        print('Error')

# Job Title Search: Returns Top Cities for Job Title
def get_results_from_db_title(user_search):
    conn = get_db_connection()
    cur = conn.cursor()
    SQL_query = "SELECT Jobs.title, Jobs.salary, Cities.name, Cities.latitude, Cities.longitude, States.name FROM Jobs INNER JOIN Cities ON Jobs.city_id = Cities.id INNER Join States ON Cities.state_id = States.id WHERE lower(Jobs.title) = (%s) ORDER BY Jobs.salary DESC LIMIT 5"
    cur.execute(SQL_query, (user_search.lower(),))
    rows = cur.fetchall()
    conn.close()

    def transform_to_object_title(row):
        return {"Job Title": row[0], "Salary": row[1], "City": row[2], "lat": float(row[3]), "lng": float(row[4]), "State": row[5]}

    holder = list(map(transform_to_object_title, rows))

    return(holder)

# State Search: Returns Top Job Titles for State
def get_results_from_db_state(user_search):
    conn = get_db_connection()
    cur = conn.cursor()
    SQL_query = "SELECT Jobs.title, Jobs.salary, Cities.name, Cities.latitude, Cities.longitude, States.name FROM Jobs INNER JOIN Cities ON Jobs.city_id = Cities.id INNER Join States ON Cities.state_id = States.id WHERE lower(States.name) = (%s) ORDER BY Jobs.salary DESC LIMIT 5"
    cur.execute(SQL_query, (user_search.lower(),))
    rows = cur.fetchall()
    conn.close()

    def transform_to_object_state(row):
        return {"Job Title": row[0], "Salary": row[1], "City": row[2], "lat": float(row[3]), "lng": float(row[4]), "State": row[5]}

    holder = list(map(transform_to_object_state, rows))

    return(holder)

# Best Cities For <Job Title> in <State>: Returns Top Cities for Job Title
def get_results_from_db_title_in_state(user_search_title, user_search_state):
    conn = get_db_connection()
    cur = conn.cursor()
    SQL_query = "SELECT Jobs.title, Jobs.salary, Cities.name, Cities.latitude, Cities.longitude, States.name FROM Jobs INNER JOIN Cities ON Jobs.city_id = Cities.id INNER Join States ON Cities.state_id = States.id WHERE lower(Jobs.title) = (%s) AND lower(States.name) = (%s) ORDER BY Jobs.salary DESC LIMIT 5"
    data = (user_search_title.lower(), user_search_state.lower())
    cur.execute(SQL_query, data)
    rows = cur.fetchall()
    conn.close()

    def transform_to_object_title_in_state(row):
        return {"Job Title": row[0], "Salary": row[1], "City": row[2], "lat": float(row[3]), "lng": float(row[4]), "State": row[5]}

    holder = list(map(transform_to_object_title_in_state, rows))

    return(holder)

# Top Jobs in <City> Route: Returns Top Jobs for City
def get_results_from_db_city(user_search):
    conn = get_db_connection()
    cur = conn.cursor()
    SQL_query = "SELECT Jobs.title, Jobs.salary, Cities.name, Cities.latitude, Cities.longitude, States.name FROM Jobs INNER JOIN Cities ON Jobs.city_id = Cities.id INNER Join States ON Cities.state_id = States.id WHERE lower(Cities.name) = (%s) ORDER BY Jobs.salary DESC LIMIT 5"
    cur.execute(SQL_query, (user_search.lower(),))
    rows = cur.fetchall()
    conn.close()

    def transform_to_object_city(row):
        return {"Job Title": row[0], "Salary": row[1], "City": row[2], "lat": float(row[3]), "lng": float(row[4]), "State": row[5]}

    holder = list(map(transform_to_object_city, rows))

    return(holder)

# Job Title Search Route
@bp.route("/searchTitle/<title>", methods=['GET'])
@cross_origin()
def search_title(title):
    return {"results": get_results_from_db_title(title)}

# State Search Route
@bp.route("/searchState/<state>", methods=['GET'])
@cross_origin()
def search_state(state):
    return {"results": get_results_from_db_state(state)}

# Best Cities For <Job Title> in <State> Route
@bp.route("/searchStateAndTitle/<title>/<state>", methods=['GET'])
@cross_origin()
def search_title_in_state(title, state):
    return {"results": get_results_from_db_title_in_state(title, state)}

# Top Jobs in <City> Route
@bp.route("/searchCity/<city>", methods=['GET'])
@cross_origin()
def search_city(city):
    return {"results": get_results_from_db_city(city)}