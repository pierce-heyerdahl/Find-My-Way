from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()

conn_string = 'postgresql://jeffbailie@localhost:5432/mydb'

class Salary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column('CITY', db.String)
    state = db.Column('STATE', db.String)
    job = db.Column('JOB TITLE', db.String)
    salary = db.Column('Annual mean wage', db.Integer)

class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    abbreviation = db.Columb(db.String)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    lattitude = db.Column(db.Double)
    longitude = db.Column(db.Double)
    state = db.Column(db.String)
    