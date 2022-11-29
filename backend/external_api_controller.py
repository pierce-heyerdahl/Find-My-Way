from flask import Blueprint
from flask_cors import cross_origin
import psycopg2
import os
import requests
import json

external_api_controller = Blueprint('external_api_controller', __name__)

DATABASE_URL = os.environ['DATABASE_URL']

def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except:
        print('Error')

def api_call(parameter):
    headers = {'Content-type': 'application/json'}
    data = json.dumps({"seriesid": [parameter],"startyear":"2021", "endyear":"2021"})
    p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
    json_res = p.json()
    value = json_res["Results"]["series"][0]["data"][0]["value"]
    return value

def seed_database():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE Cities (id INT PRIMARY KEY, name VARCHAR(45), geolocation VARCHAR(45), cpi_region INT, cpi_val INT, state_id INT)")
    cur.execute("CREATE TABLE States (id INT PRIMARY KEY, name VARCHAR(45), country VARCHAR(45))")
    cur.execute("CREATE TABLE Jobs (id INT PRIMARY KEY, title VARCHAR(45), city_id INT, state_id INT, num_jobs INT, salary INT, status VARCHAR(45), FOREIGN KEY (city_id) REFERENCES Cities(id))")
    conn.commit()
    cur.execute("INSERT INTO Cities (id, name) VALUES (1, 'Seattle'), (2, 'Olympia'), (3, 'Bellingham'), (4, 'Kennewick'), (5, 'Spokane')")

    # BLS API call for Bellingham WA
    value = api_call("OEUM001338000000015125404")
    SQL_query = "INSERT INTO Jobs (id, title, salary, city_id) VALUES (1, 'Web Developer', (%s), 3)"
    cur.execute(SQL_query, (value,))

    # BLS API call for Kennewick WA
    value = api_call("OEUM002842000000015125404")
    SQL_query = "INSERT INTO Jobs (id, title, salary, city_id) VALUES (2, 'Web Developer', (%s), 4)"
    cur.execute(SQL_query, (value,))

    # BLS API call for Olympia
    value = api_call("OEUM003650000000015125404")
    SQL_query = "INSERT INTO Jobs (id, title, salary, city_id) VALUES (3, 'Web Developer', (%s), 2)"
    cur.execute(SQL_query, (value,))

    # BLS API call for Seattle
    value = api_call("OEUM004266000000015125404")
    SQL_query = "INSERT INTO Jobs (id, title, salary, city_id) VALUES (4, 'Web Developer', (%s), 1)"
    cur.execute(SQL_query, (value,))

    # BLS API call for Spokane
    value = api_call("OEUM004406000000015125404")
    SQL_query = "INSERT INTO Jobs (id, title, salary, city_id) VALUES (5, 'Web Developer', (%s), 5)"
    cur.execute(SQL_query, (value,))

    conn.commit()
    conn.close()

@external_api_controller.route("/seed")
@cross_origin()
def seed():
    seed_database()
    return ("Success")