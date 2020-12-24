from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_URL = 'postgresql://app:money@localhost:5432'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)
app.config.from_object(__name__)

from app import views
from app import models


def init_db():
    db.create_all()


def reset_db():
    db.drop_all()
    db.create_all()
