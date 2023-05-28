from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()


class Salary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String)
    state = db.Column(db.String)
    abbr = db.Column(db.String)
    job = db.Column(db.String)
    salary = db.Column(db.Integer)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    state = db.Column(db.String)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    abbr = db.Column(db.String)

class CityCol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String)
    state = db.Column(db.String)
    coli = db.Column(db.Float)
    
class StateCol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String)
    coli = db.Column(db.Float)
    