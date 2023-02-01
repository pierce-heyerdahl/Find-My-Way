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

def get_results_from_db(user_search):
    conn = get_db_connection()
    cur = conn.cursor()
    SQL_query = "SELECT Jobs.title, Jobs.salary, Cities.name, Cities.latitude, Cities.longitude FROM Jobs INNER JOIN Cities ON Jobs.city_id = Cities.id WHERE lower(Jobs.title) = (%s) ORDER BY Jobs.salary DESC LIMIT 5"
    cur.execute(SQL_query, (user_search.lower(),))
    rows = cur.fetchall()
    conn.close()

    def transform_to_object(row):
        return {"Job Title": row[0], "Salary": row[1], "City": row[2], "lat": float(row[3]), "lng": float(row[4])}

    holder = list(map(transform_to_object, rows))

    return(holder)

@bp.route("/search/<state>", methods=['GET'])
@cross_origin()
def search(state):
    return {"results": get_results_from_db(state)}