from flask import Blueprint
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import psycopg2
import os
from sqlalchemy import select
from models import *

bp = Blueprint('front_end_api_controller_bp', __name__)

def get_results_from_db_title(user_search):
    query = (
        select(Salary, City)
        .where(Salary.job == user_search)
        .join_from(Salary, City, (Salary.state == City.state) & (Salary.city == City.name))
        .order_by(Salary.salary.desc())
        .limit(5)
    ) 

    results = db.session.execute(query)

    #funciton to tranform result set to object
    def transform_to_object(row):
        salary_res = row[0]
        city_res = row[1]
        return {"Job Title": salary_res.job, "Salary": salary_res.salary, "City": salary_res.city, "lat": city_res.lat, "lng": city_res.lng, "State": salary_res.state}

    holder = list(map(transform_to_object, results))

    return(holder)

def get_results_from_db_state(user_search):

    query = (
        select(Salary, City)
        .where((Salary.state == user_search) | (Salary.abbr == user_search))
        .join_from(Salary, City, (Salary.state == City.state) & (Salary.city == City.name))
        .order_by(Salary.salary.desc())
        .limit(5)
    ) 
    results = db.session.execute(query)

    #funciton to tranform result set to object
    def transform_to_object(row):
        salary_res = row[0]
        city_res = row[1]
        return {"Job Title": salary_res.job, "Salary": salary_res.salary, "City": salary_res.city, "lat": city_res.lat, "lng": city_res.lng, "State": salary_res.state}

    holder = list(map(transform_to_object, results))

    return(holder)

def get_results_from_db_title_in_state(user_search_job, user_search_state):
    query = (
        select(Salary, City)
        .where((Salary.job == user_search_job) & (Salary.state == user_search_state))
        .join_from(Salary, City, (Salary.state == City.state) & (Salary.city == City.name))
        .order_by(Salary.salary.desc())
        .limit(5)
    ) 

    results = db.session.execute(query)

    #funciton to tranform result set to object
    def transform_to_object(row):
        salary_res = row[0]
        city_res = row[1]
        return {"Job Title": salary_res.job, "Salary": salary_res.salary, "City": salary_res.city, "lat": city_res.lat, "lng": city_res.lng, "State": salary_res.state}

    holder = list(map(transform_to_object, results))

    return(holder)


def get_results_from_db_city(user_search):
    query = (
        select(Salary, City)
        .where(Salary.city == user_search)
        .join_from(Salary, City, (Salary.state == City.state) & (Salary.city == City.name))
        .order_by(Salary.salary.desc())
        .limit(5)
    ) 

    results = db.session.execute(query)

    #funciton to tranform result set to object
    def transform_to_object(row):
        salary_res = row[0]
        city_res = row[1]
        return {"Job Title": salary_res.job, "Salary": salary_res.salary, "City": salary_res.city, "lat": city_res.lat, "lng": city_res.lng, "State": salary_res.state}

    holder = list(map(transform_to_object, results))

    return(holder)

@bp.route("/searchState/<state>", methods=['GET'])
@cross_origin()
def search_state(state):
    return {"results": get_results_from_db_state(state)}

@bp.route("/searchTitle/<title>", methods=['GET'])
@cross_origin()
def search_title(title):
    return {"results": get_results_from_db_title(title)}

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
