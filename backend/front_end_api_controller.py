from flask import Blueprint
from flask_cors import cross_origin
from sqlalchemy import select, func
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

@bp.route('/CitiesListV2', strict_slashes = False, methods =['GET'])
@cross_origin()
def v2_list_cities():
    query = select(Salary.city, Salary.state).distinct()
    results = db.session.execute(query).all()
    results = [{'city': row[0], 'state': row[1]} for row in results]
    return {'cities': results}

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

@bp.route("/search/<title>/<state>/<city>/<minSalary>/<maxSalary>/<page>", methods=['GET'])
@cross_origin()
# If user didnt fill out certain search parameters they will be passed in as "null"
# all this code is just example you can modify/delete
def search(title, state, city, minSalary, maxSalary, page):

    items_per_page = 10
    if page != "null":
        page = int(page)
    else:
        page = 1

    query = select(Salary, City)

    if title != "null":
        query = query.filter(Salary.job.ilike(f'%{title}%'))
    
    if state != "null":
        query = query.filter((Salary.state.ilike(f'{state}')) | (Salary.abbr.ilike(f'{state}')))

    if city != "null":
        query = query.filter(Salary.city.ilike(f'%{city}%'))

    if (minSalary != "null") and (maxSalary != "null"):
        query = query.where((Salary.salary >= minSalary) & (Salary.salary <= maxSalary))

    query = query.join_from(Salary, City, (Salary.state == City.state) & (Salary.city == City.name)).order_by(Salary.salary.desc())

    total_query = query.with_only_columns([func.count()]).order_by(None)
    total_results = db.session.execute(total_query).scalar()
    # alt ceil implementation
    total_pages = -(-total_results // items_per_page)

    offset = (page - 1) * items_per_page
    query = query.offset(offset).limit(items_per_page)
    
    results = db.session.execute(query)

    #funciton to tranform result set to object
    def transform_to_object(row):
        salary_res = row[0]
        city_res = row[1]
        return {"Job Title": salary_res.job, "Salary": salary_res.salary, "City": salary_res.city, "lat": city_res.lat, "lng": city_res.lng, "State": salary_res.abbr}

    holder = list(map(transform_to_object, results))

    return {"results": holder, "total_pages": total_pages}
