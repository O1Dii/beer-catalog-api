import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db_owner = os.getenv('DATABASE_OWNER')
db_password = os.getenv('DATABASE_PASSWORD')
db_addr = os.getenv('DATABASE_ADDR')
db_name = os.getenv('DATABASE_NAME')
base_url = os.getenv('BASE_URL')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_owner}:{db_password}@{db_addr}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from api.models import *
