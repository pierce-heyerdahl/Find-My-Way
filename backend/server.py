from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask.helpers import send_from_directory
from dotenv import load_dotenv
#import psycopg2
#import os
#import requests
#import json

from front_end_api_controller import front_end_api_controller
from external_api_controller import external_api_controller

# loading environmental variables
#load_dotenv()

# getting credentials for database
# for local
#DATABASE = os.getenv('DATABASE')
#DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
#DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')

# for production
#DATABASE_URL = os.environ['DATABASE_URL']

app = Flask(__name__, static_folder = '../frontend/build/', static_url_path = '/')

app.register_blueprint(front_end_api_controller)
app.register_blueprint(external_api_controller)

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
#def get_db_connection():
#    try:
#        conn = psycopg2.connect("postgres://mafdqjmmyxvdwg:222f4ef14563eaf40662009e9f6e9b3d094d21800fcf694e0b0707710b3ed40a@ec2-52-73-184-24.compute-1.amazonaws.com:5432/d4f8k8hv1t3g5q")
#        return conn
#    except:
#        print('Error')

@app.route("/")
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/test", methods=['GET'])
@cross_origin()
def numbers():
    return {"numbers": ["four", "five"]}

if __name__ == "__main__":
    #app.run(host = "0.0.0.0", debug = True, port = int(os.environ.get("PORT", 5000)))
    app.run()