from flask import Blueprint
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import psycopg2
import os
from sqlalchemy import select
from models import *

bp = Blueprint('front_end_api_controller_bp', __name__)

def get_results_from_db_title(user_search):
    query = select(Salary).where(Salary.job == user_search).order_by(Salary.salary.desc()).limit(5)
    results = db.session.execute(query)

    #funciton to tranform result set to object
    def transform_to_object(row):
        salary_res = row[0]
        return {"Job Title": salary_res.job, "Salary": salary_res.salary, "City": salary_res.city}

    holder = list(map(transform_to_object, results))

    return(holder)

def get_results_from_db_state(user_search):
    query = select(Salary).where(Salary.state == user_search).order_by(Salary.salary.desc()).limit(5)
    results = db.session.execute(query)

    #funciton to tranform result set to object
    def transform_to_object(row):
        salary_res = row[0]
        return {"Job Title": salary_res.job, "Salary": salary_res.salary, "City": salary_res.city}

    holder = list(map(transform_to_object, results))

    return(holder)

@bp.route("/searchState/<state>", methods=['GET'])
@cross_origin()
def search(state):
    return {"results": get_results_from_db_state(state)}

@bp.route("/searchTitle/<title>", methods=['GET'])
@cross_origin()
def search(title):
    return {"results": get_results_from_db_title(title)}