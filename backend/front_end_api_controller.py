from flask import Blueprint
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import psycopg2
import os
from sqlalchemy import select
from models import *
from state_to_abreviation import abbrevStates

bp = Blueprint('front_end_api_controller_bp', __name__)

@bp.route('/CitiesList/<cityInput>', methods = ['GET'])
@cross_origin()
def list_cities_contain(cityInput):
    query = select(Salary.city, Salary.state).filter(Salary.city.ilike(f'%{cityInput}%')).distinct()
    results = db.session.execute(query).all()
    results = {row[0]: row[1] for row in results}
    return results

@bp.route('/CitiesList', strict_slashes = False, methods = ['GET'])
@cross_origin()
def list_cities():
    query = select(Salary.city, Salary.state).distinct()
    results = db.session.execute(query).all()
    results = {row[0]: row[1] for row in results}
    return results
    
@bp.route('/JobsList', strict_slashes = False, methods = ['GET'])
@cross_origin()
def list_job_titles():
    query = select(Salary.job).distinct()
    results = db.session.execute(query).all()
    results = [row[0] for row in results]
    return results

@bp.route('/JobsList/<jobInput>', methods = ['GET'])
@cross_origin()
def list_job_titles_contains(jobInput):
    query = select(Salary.job).filter(Salary.job.ilike(f'%{jobInput}%')).distinct()
    results = db.session.execute(query).all()
    results = [row[0] for row in results]
    return results

@bp.route('/StatesList', strict_slashes = False, methods = ['GET'])
@cross_origin()
def list_states():
    return abbrevStates

# Combined route for single search
@bp.route("/search/<title>/<state>/<city>/<minSalary>/<maxSalary>", methods=['GET'])
@cross_origin()
# If user didnt fill out certain search parameters they will be passed in as "null"
# all this code is just example you can modify/delete
def search(title, state, city, minSalary, maxSalary):
    query = select(Salary, City)

    if title != "null":
        query = query.filter(Salary.job.ilike(f'%{title}%'))
    
    if state != "null":
        query = query.filter((Salary.state.ilike(f'^{state}%')) | (Salary.abbr.ilike(f'^{state}%')))

    if city != "null":
        query = query.filter(Salary.city.ilike(f'%{city}%'))

    if (minSalary != "null") and (maxSalary != "null"):
        query = query.where((Salary.salary >= minSalary) & (Salary.salary <= maxSalary))
    
    query = query.join_from(Salary, City, (Salary.state == City.state) & (Salary.city == City.name)).order_by(Salary.salary.desc()).limit(10)
    
    results = db.session.execute(query)

    #funciton to tranform result set to object
    def transform_to_object(row):
        salary_res = row[0]
        city_res = row[1]
        return {"Job Title": salary_res.job, "Salary": salary_res.salary, "City": salary_res.city, "lat": city_res.lat, "lng": city_res.lng, "State": salary_res.abbr}

    holder = list(map(transform_to_object, results))

    return {"results": holder}
