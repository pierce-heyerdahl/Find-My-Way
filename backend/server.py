from flask import Flask, jsonify, request
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
#DATABASE = os.getenv('DATABASE')
#DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
#DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_URL = os.environ['DATABASE_URL']

app = Flask(__name__, static_folder = '../frontend/build/', static_url_path = '/')
CORS(app)

# for local
#def get_db_connection():
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

# old version
# def seed_database():
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute('CREATE TABLE states (state_id INT PRIMARY KEY, state_name VARCHAR(45))')
#     conn.commit()
#     cur.execute("INSERT INTO states (state_id, state_name) VALUES (1, 'Washington'), (2, 'Oregon')")
#     conn.commit()
#     conn.close()

def seed_database():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE Cities (id INT PRIMARY KEY, name VARCHAR(45), geolocation VARCHAR(45), cpi_region INT, cpi_val INT, state_id INT)")
    conn.commit()
    cur.execute("CREATE TABLE Jobs (id INT PRIMARY KEY, title VARCHAR(45), city_id INT, state_id INT, num_jobs INT, salary INT, status VARCHAR(45), FOREIGN KEY (city_id) REFERENCES Cities(id))")
    conn.commit()
    cur.execute("INSERT INTO Cities (id, name) VALUES (1, 'Seattle')")
    cur.execute("INSERT INTO Cities (id, name) VALUES (2, 'Olympia')")
    cur.execute("INSERT INTO Jobs (id, title, salary, city_id) VALUES (1, 'Web Developer', 100000, 1)")
    cur.execute("INSERT INTO Jobs (id, title, salary, city_id) VALUES (4, 'Web Developer', 99000, 2)")
    cur.execute("INSERT INTO Jobs (id, title, salary, city_id) VALUES (2, 'Programmer', 75000, 1)")
    cur.execute("INSERT INTO Jobs (id, title, salary, city_id) VALUES (3, 'KFC Manager', 50000, 1)")
    conn.commit()
    conn.close()

def test_connection():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM states')
    rows = cur.fetchall()
    conn.close()
    return(rows)

def get_results_from_db(user_search):
    conn = get_db_connection()
    cur = conn.cursor()
    # old query
    #SQL_query = "SELECT * FROM states WHERE states.state_name=(%s)"
    SQL_query = "SELECT Jobs.title, Jobs.salary, Cities.name FROM Jobs INNER JOIN Cities ON Jobs.city_id = Cities.id WHERE Jobs.title=(%s) ORDER BY Jobs.salary DESC"
    cur.execute(SQL_query, (user_search,))
    rows = cur.fetchall()
    conn.close()

    def transform_to_object(row):
        return {"Job Title": row[0], "Salary": row[1], "City": row[2]}

    holder = list(map(transform_to_object, rows))

    return(holder)

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

@app.route("/search/<state>", methods=['GET'])
@cross_origin()
def search(state):
    return {"results": get_results_from_db(state)}

@app.route("/seed")
@cross_origin()
def seed():
    seed_database()
    return ("Success")

# route to call BLS api
@app.route("/api", methods=['GET'])
@cross_origin()
def apiCall():

    # API call to BLS to get annual mean salary for web developers in , Bellingham WA, Kennewick-Richland WA, Olympia-Tumwater WA, Seattle-Tacoma-Bellevue WA, Spokane-Spokane Valley WA (In That Order)
    headers = {'Content-type': 'application/json'}
    data = json.dumps({"seriesid": ['OEUM001338000000015125404','OEUM002842000000015125404','OEUM003650000000015125404','OEUM004266000000015125404','OEUM004406000000015125404'],"startyear":"2021", "endyear":"2021"})
    p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
    json_res = p.json()

    return (json_res)

if __name__ == "__main__":
    #app.run(host = "0.0.0.0", debug = True, port = int(os.environ.get("PORT", 5000)))
    app.run()
