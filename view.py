import json
import os

from app import models
from flask import (
  Flask,
  render_template,
  Response)
from flask.ext.sqlalchemy import SQLAlchemy
from app.models import Prescription


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
    'postgresql+psycopg2://awvolathokychi:SfaeRpVGxZowm_K7IDkTGvEvcM' +
    '@ec2-23-23-95-222.compute-1.amazonaws.com' +
    ':5432/d6p5qsqchkuarn')
db = models.db

@app.route('/')
def hello():
  return render_template('index.html')

@app.route('/users/<int:user_id>/prescriptions', methods=['GET'])
def getPrescriptions(user_id):
  prescriptions = db.session.query(Prescription).filter(Prescription.patient_id == user_id)
  json_str = json.dumps({'Prescriptions': [models.serialize(prescription) for prescription in prescriptions]}, default=models.custom_parser)
  resp = Response(json_str, status=200, mimetype='application/json')
  return resp

@app.route('/users/<int:user_id>', methods=['GET'])
def getUserData(user_id):
  user = models.User.query.get(user_id)
  resp = Response(json.dumps({'User': models.serialize(user)}), status=200)
  resp.mimetype = 'application/json'
  return resp
