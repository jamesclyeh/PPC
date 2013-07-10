import datetime
import json
import os

from app import models
from flask import (
  Flask,
  render_template,
  request,
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

@app.route('/updateInventory', methods=['PUT'])
def updateInventory():
  prescription_id = request.json['prescription_id']
  refill_amount = request.json.get('refill', 0)
  latest_record = db.session.query(models.DrugInventory).order_by(models.DrugInventory.time_stamp.desc())[0]
  prescription = Prescription.query.get(prescription_id)
  new_amount = latest_record.inventory + refill_amount if refill_amount else latest_record.inventory - prescription.dosage
  record = models.DrugInventory(prescription_id, new_amount, datetime.datetime.now())
  db.session.add(record)
  db.session.commit()
  return Response('', status=200)
