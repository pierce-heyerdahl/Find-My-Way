from flask import Blueprint
from flask_cors import cross_origin
from dotenv import load_dotenv
import psycopg2
import os
import requests
import json

bp = Blueprint('external_api_controller_bp', __name__)

#local DB
#load_dotenv()
#DATABASE = os.getenv('DATABASE')
#DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
#DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
#registrationkey = os.getenv('REGISTRATION_KEY')

#production DB
DATABASE_URL = os.environ['DATABASE_URL']
registrationkey = os.environ['REGISTRATION_KEY']

def get_db_connection():
    try:
        #local DB
        #conn = psycopg2.connect(database = DATABASE, user = DATABASE_USERNAME, password = DATABASE_PASSWORD)

        #production DB
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except:
        print('Error')

def api_call(parameter):
    headers = {'Content-type': 'application/json'}
    data = json.dumps({"seriesid": [parameter],"startyear":"2021", "endyear":"2021", "registrationkey":registrationkey})
    p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
    json_res = p.json()
    value = json_res["Results"]["series"][0]["data"][0]["value"]
    return value

def seed_database():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Cities (id INT PRIMARY KEY, name VARCHAR(45), latitude NUMERIC, longitude NUMERIC, cpi_region INT, cpi_val INT, state_id INT)")
    cur.execute("CREATE TABLE IF NOT EXISTS States (id INT PRIMARY KEY, name VARCHAR(45), country VARCHAR(45))")
    cur.execute("CREATE TABLE IF NOT EXISTS Jobs (id INT PRIMARY KEY, title VARCHAR(45), city_id INT, state_id INT, num_jobs INT, salary INT, status VARCHAR(45), FOREIGN KEY (city_id) REFERENCES Cities(id))")
    conn.commit()
    cur.execute("INSERT INTO Cities (id, name, latitude, longitude, state_id) VALUES (1, 'Bellingham', 48.769768, -122.485886, 1), (2, 'Bremerton', 47.5687, -122.6515, 1), (3, 'Kennewick', 46.2022, -119.1555, 1), (4, 'Longview', 46.1382, -122.9382, 1), (5, 'Mount Vernon', 48.4212, -122.3341, 1), (6, 'Olympia', 47.037872, -122.900696, 1), (7, 'Seattle', 47.608013, -122.335167, 1), (8, 'Spokane', 47.658779, -117.426048, 1), (9, 'Walla Walla', 46.064583, -118.343018, 1), (10, 'Wenatchee', 47.423458, -120.310349, 1), (11, 'Yakima', 46.602070, -120.505898, 1)")
    cur.execute("INSERT INTO Cities (id, name, latitude, longitude, state_id) VALUES (12, 'Portland', 45.523, -122.676, 2)")
    cur.execute("INSERT INTO States (id, name) VALUES (1, 'Washington'), (2, 'Oregon'), (3, 'California'), (4, 'Idaho'), (5, 'Nevada')")

    # BLS API call for Bellingham WA for Web Developer
    value = api_call("OEUM001338000000015125404")
    SQL_query = "INSERT INTO Jobs (id, title, salary, city_id) VALUES (1, 'Web Developer', (%s), 1)"
    cur.execute(SQL_query, (value,))

    # BLS API call for Kennewick WA for Web Developer
    value = api_call("OEUM002842000000015125404")
    SQL_query = "INSERT INTO Jobs (id, title, salary, city_id) VALUES (2, 'Web Developer', (%s), 3)"
    cur.execute(SQL_query, (value,))

    # BLS API call for Olympia WA for Web Developer
    value = api_call("OEUM003650000000015125404")
    SQL_query = "INSERT INTO Jobs (id, title, salary, city_id) VALUES (3, 'Web Developer', (%s), 6)"
    cur.execute(SQL_query, (value,))

    # BLS API call for Seattle WA for Web Developer
    value = api_call("OEUM004266000000015125404")
    SQL_query = "INSERT INTO Jobs (id, title, salary, city_id) VALUES (4, 'Web Developer', (%s), 7)"
    cur.execute(SQL_query, (value,))

    # BLS API call for Spokane WA for Web Developer
    value = api_call("OEUM004406000000015125404")
    SQL_query = "INSERT INTO Jobs (id, title, salary, city_id) VALUES (5, 'Web Developer', (%s), 8)"
    cur.execute(SQL_query, (value,))

    # BLS API call for Bellingham WA for Lawyer
    value = api_call("OEUM001338000000023101104")
    SQL_query = "INSERT INTO Jobs (id, title, salary, city_id) VALUES (6, 'Lawyer', (%s), 1)"
    cur.execute(SQL_query, (value,))

    # BLS API call for Bremerton WA for Lawyer
    value = api_call("OEUM001474000000023101104")
    SQL_query = "INSERT INTO Jobs (id, title, salary, city_id) VALUES (7, 'Lawyer', (%s), 2)"
    cur.execute(SQL_query, (value,))

    # BLS API call for Kennewick WA for Lawyer
    value = api_call("OEUM002842000000023101104")
    SQL_query = "INSERT INTO Jobs (id, title, salary, city_id) VALUES (8, 'Lawyer', (%s), 3)"
    cur.execute(SQL_query, (value,))

    # BLS API call for Longview WA for Lawyer
    value = api_call("OEUM003102000000023101104")
    SQL_query = "INSERT INTO Jobs (id, title, salary, city_id) VALUES (9, 'Lawyer', (%s), 4)"
    cur.execute(SQL_query, (value,))

    # BLS API call for Mount Vernon WA for Lawyer
    value = api_call("OEUM003458000000023101104")
    SQL_query = "INSERT INTO Jobs (id, title, salary, city_id) VALUES (10, 'Lawyer', (%s), 5)"
    cur.execute(SQL_query, (value,))

    # BLS API call for Olympia WA for Lawyer
    value = api_call("OEUM003650000000023101104")
    SQL_query = "INSERT INTO Jobs (id, title, salary, city_id) VALUES (11, 'Lawyer', (%s), 6)"
    cur.execute(SQL_query, (value,))

    # BLS API call for Seattle WA for Lawyer
    value = api_call("OEUM004266000000023101104")
    SQL_query = "INSERT INTO Jobs (id, title, salary, city_id) VALUES (12, 'Lawyer', (%s), 7)"
    cur.execute(SQL_query, (value,))

    # BLS API call for Spokane WA for Lawyer
    value = api_call("OEUM004406000000023101104")
    SQL_query = "INSERT INTO Jobs (id, title, salary, city_id) VALUES (13, 'Lawyer', (%s), 8)"
    cur.execute(SQL_query, (value,))

    # BLS API call for Walla Walla WA for Lawyer
    value = api_call("OEUM004746000000023101104")
    SQL_query = "INSERT INTO Jobs (id, title, salary, city_id) VALUES (14, 'Lawyer', (%s), 9)"
    cur.execute(SQL_query, (value,))

    # BLS API call for Wenatchee WA for Lawyer
    value = api_call("OEUM004830000000023101104")
    SQL_query = "INSERT INTO Jobs (id, title, salary, city_id) VALUES (15, 'Lawyer', (%s), 10)"
    cur.execute(SQL_query, (value,))

    # BLS API call for Yakima WA for Lawyer
    value = api_call("OEUM004942000000023101104")
    SQL_query = "INSERT INTO Jobs (id, title, salary, city_id) VALUES (16, 'Lawyer', (%s), 11)"
    cur.execute(SQL_query, (value,))

    # Dummy Data for State Search test
    cur.execute("INSERT INTO Jobs (id, title, salary, city_id) VALUES (17, 'Cashier', 55000, 12)")
    cur.execute("INSERT INTO Jobs (id, title, salary, city_id) VALUES (18, 'Clerk', 45000, 12)")
    cur.execute("INSERT INTO Jobs (id, title, salary, city_id) VALUES (19, 'Mechanic', 60000, 12)")
    cur.execute("INSERT INTO Jobs (id, title, salary, city_id) VALUES (20, 'Programmer', 80000, 12)")
    cur.execute("INSERT INTO Jobs (id, title, salary, city_id) VALUES (21, 'Actor', 100000, 12)")
    cur.execute("INSERT INTO Jobs (id, title, salary, city_id) VALUES (22, 'Dentist', 120000, 12)")


    conn.commit()
    conn.close()

@bp.route("/seed")
@cross_origin()
def seed():
    seed_database()
    return ("Success")