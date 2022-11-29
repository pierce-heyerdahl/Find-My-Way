from flask import Blueprint
from flask_cors import cross_origin
import psycopg2
import os
import requests
import json

bp = Blueprint('external_api_controller_bp', __name__)

DATABASE_URL = os.environ['DATABASE_URL']
registrationkey = os.environ['REGISTRATION_KEY']

def get_db_connection():
    try:
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
    cur.execute("CREATE TABLE IF NOT EXIST Cities (id INT PRIMARY KEY, name VARCHAR(45), geolocation VARCHAR(45), cpi_region INT, cpi_val INT, state_id INT)")
    cur.execute("CREATE TABLE IF NOT EXIST States (id INT PRIMARY KEY, name VARCHAR(45), country VARCHAR(45))")
    cur.execute("CREATE TABLE IF NOT EXIST Jobs (id INT PRIMARY KEY, title VARCHAR(45), city_id INT, state_id INT, num_jobs INT, salary INT, status VARCHAR(45), FOREIGN KEY (city_id) REFERENCES Cities(id))")
    conn.commit()
    cur.execute("INSERT INTO Cities (id, name) VALUES (1, 'Bellingham'), (2, 'Bremerton'), (3, 'Kennewick'), (4, 'Longview'), (5, 'Mount Vernon'), (6, 'Olympia'), (7, 'Seattle'), (8, 'Spokane'), (9, 'Walla Walla'), (10, 'Wenatchee'), (11, 'Yakima')")

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

    conn.commit()
    conn.close()

@bp.route("/seed")
@cross_origin()
def seed():
    seed_database()
    return ("Success")