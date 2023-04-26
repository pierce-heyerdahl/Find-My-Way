from flask import Blueprint
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import psycopg2
import os
from sqlalchemy import select
from models import *


bp = Blueprint('db_admin_upload_api', __name__)