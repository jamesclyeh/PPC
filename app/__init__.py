import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
           'postgresql+psycopg2://awvolathokychi:SfaeRpVGxZowm_K7IDkTGvEvcM' +
           '@ec2-23-23-95-222.compute-1.amazonaws.com' +
           ':5432/d6p5qsqchkuarn')
db = SQLAlchemy(app)

from app import models
