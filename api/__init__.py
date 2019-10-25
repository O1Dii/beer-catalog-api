import os

from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

db_owner = os.getenv('DATABASE_OWNER')
db_password = os.getenv('DATABASE_PASSWORD')
db_addr = os.getenv('DATABASE_ADDR')
db_name = os.getenv('DATABASE_NAME')
base_url = os.getenv('BASE_URL')

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_owner}:{db_password}@{db_addr}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

from api.models import *
from api.routes import *
from api.cli_commands import *
