import json
import os

from app import models
from flask import Flask, render_template, Response
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
    'postgresql+psycopg2://awvolathokychi:SfaeRpVGxZowm_K7IDkTGvEvcM' +
    '@ec2-23-23-95-222.compute-1.amazonaws.com' +
    ':5432/d6p5qsqchkuarn')

@app.route('/')
def hello():
  return render_template('index.html')

@app.route('/viewUsers', methods=['GET'])
def dbTest():
  users = models.User.query.all()
  prescriptions = models.Prescription.query.all()
  ret_str = json.dumps({'Users': [models.serialize(user) for user in users]}) + '<br>'
  ret_str += json.dumps({'Prescriptions': [models.serialize(prescription) for prescription in prescriptions]}, default=models.custom_parser) + '<br>'
  response = ret_str
  resp = Response(ret_str, status=200, mimetype='application/json')
  return resp
