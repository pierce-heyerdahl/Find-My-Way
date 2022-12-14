from flask import Blueprint
from flask_cors import CORS, cross_origin
import psycopg2
import os

bp = Blueprint('front_end_api_controller_bp', __name__)

DATABASE_URL = os.environ['DATABASE_URL']

def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except:
        print('Error')

def get_results_from_db(user_search):
    conn = get_db_connection()
    cur = conn.cursor()
    SQL_query = "SELECT Jobs.title, Jobs.salary, Cities.name FROM Jobs INNER JOIN Cities ON Jobs.city_id = Cities.id WHERE Jobs.title=(%s) ORDER BY Jobs.salary DESC LIMIT 5"
    cur.execute(SQL_query, (user_search,))
    rows = cur.fetchall()
    conn.close()

    def transform_to_object(row):
        return {"Job Title": row[0], "Salary": row[1], "City": row[2]}

    holder = list(map(transform_to_object, rows))

    return(holder)

@bp.route("/search/<state>", methods=['GET'])
@cross_origin()
def search(state):
    return {"results": get_results_from_db(state)}