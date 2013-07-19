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
  prescription_id = int(request.json['prescription_id'])
  prescription = models.Prescription.query.get(prescription_id)
  refill_amount = request.json.get('refill', 0)
  records = db.session.query(models.DrugInventory)\
    .filter(models.DrugInventory.prescription_id==prescription_id)\
    .order_by(models.DrugInventory.time_stamp.desc()).all()
  latest_record = None
  if len(records) > 0:
    latest_record = records[0]
  current_inventory = latest_record.inventory if latest_record else 0
  new_amount = current_inventory + refill_amount if refill_amount else None
  if latest_record:
    new_amount = current_inventory - prescription.dosage
  print new_amount
  if new_amount:
    prescription = Prescription.query.get(prescription_id)
    record = models.DrugInventory(prescription_id, new_amount, datetime.datetime.now())
    db.session.add(record)
    db.session.commit()
    return Response(str(record.prescription_id) + ':' + str(record.inventory), status=200)

@app.route('/prescriptions/<int:prescription_id>/inventory', methods=['GET'])
def getInventory(prescription_id):
  latest_record = db.session.query(models.DrugInventory)\
    .filter(models.DrugInventory.prescription_id==prescription_id)\
    .order_by(models.DrugInventory.time_stamp.desc())[0]
  return Response(str(latest_record.inventory), status=200)

@app.route('/prescriptions/<int:prescription_id>/consumption_history', methods=['GET'])
def getConsumptionHistory(prescription_id):
  records = db.session.query(models.DrugInventory)\
    .filter(models.DrugInventory.prescription_id==prescription_id)\
    .order_by(models.DrugInventory.time_stamp.desc())
  json_str = json.dumps({'ConsumptionHistory': [models.serialize(record) for record in records]}, default=models.custom_parser)
  return Response(json_str, status=200, mimetype='application/json')

@app.route('/prescription/<int:prescription_id>/update', methods=['PUT'])
def updatePrescription(prescription_id):
  record = models.Prescription.query.get(prescription_id)
  for key, value in request.json.iteritems():
    setattr(record, key, value)
  db.session.save(record)
  db.session.commit()
  return Response('', status=200)

@app.route('/prescription/insert', methods=['POST'])
def addPrescription():
  record = models.Prescription()
  for key, value in request.json.iteritems():
    setattr(record, key, value)
  db.session.add(record)
  db.session.commit()
  return Response('', status=200)
