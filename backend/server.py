from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from flask.helpers import send_from_directory
from dotenv import load_dotenv
import psycopg2
import os
import requests
import json

# loading environmental variables
load_dotenv()

# getting credentials for database
DATABASE = os.getenv('DATABASE')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_URL = os.environ['DATABASE_URL']

app = Flask(__name__, static_folder = '../frontend/build/', static_url_path = '/')
CORS(app)

# for local
# def get_db_connection():
#    try:
#        conn = psycopg2.connect(
#                database = DATABASE,
#                user = DATABASE_USERNAME,
#                password = DATABASE_PASSWORD)
#        return conn
#    except:
#        print('Error')

# for production
def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except:
        print('Error')

def seed_database():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('CREATE TABLE states (state_id INT PRIMARY KEY, state_name VARCHAR(45))')
    conn.commit()
    cur.execute("INSERT INTO states (state_id, state_name) VALUES (1, 'Washington')")
    conn.commit()
    conn.close()

def test_connection():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM states')
    rows = cur.fetchall()
    conn.close()
    return(rows)

@app.route("/")
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/test", methods=['GET'])
@cross_origin()
def numbers():
    return {"numbers": ["four", "five"]}

@app.route("/database")
@cross_origin()
def database():
    return test_connection()

@app.route("/seed")
@cross_origin()
def seed():
    seed_database()
    return ("Success")

# route to call BLS api
@app.route("/api")
@cross_origin()
def apiCall():
    headers = {'Content-type': 'application/json'}
    data = json.dumps({"seriesid": ['CUUR0000SA0'],"startyear":"2010", "endyear":"2019"})
    response = requests.get('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)
    json_res = response.json()
    return (json_res)

if __name__ == "__main__":
    #app.run(host = "0.0.0.0", debug = True, port = int(os.environ.get("PORT", 5000)))
    app.run()
