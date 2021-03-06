import datetime
import time

from app import db
from sqlalchemy.orm import class_mapper

CAREGIVER = 0
PATIENT = 1

class User(db.Model):
  __tablename__ = 'user'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64), index=True, unique=True)
  role = db.Column(db.Integer)
  email = db.Column(db.String(120), unique=True)
  phone_number = db.Column(db.String(32))

  def __init__(self, name, role, email, phone_number):
    self.name = name
    self.role = role
    self.email = email
    self.phone_number = phone_number

class Prescription(db.Model):
  __tablename__ = 'prescription'
  id = db.Column(db.Integer, primary_key=True)
  patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
  caregiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
  drug = db.Column(db.String(120))
  consumption_interval = db.Column(db.Integer)
  dosage = db.Column(db.Integer)
  start_date = db.Column(db.DateTime)
  end_date = db.Column(db.DateTime)
  __table_args__ = (db.UniqueConstraint('patient_id', 'drug'),)

  def __init__(self, patient_id=1, caregiver_id=2, drug=None, consumption_interval=None, dosage=None, start_date=None, end_date=None):
    self.patient_id = patient_id
    self.caregiver_id = caregiver_id
    self.drug = drug
    self.consumption_interval = consumption_interval
    self.dosage = dosage
    self.start_date = start_date
    self.end_date = end_date

class ArchivedPrescription(db.Model):
  __tablename__ = 'archived_prescription'
  id = db.Column(db.Integer, primary_key=True)
  patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
  caregiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
  drug = db.Column(db.String(120))
  consumption_interval = db.Column(db.Integer)
  dosage = db.Column(db.Integer)
  start_date = db.Column(db.DateTime)
  end_date = db.Column(db.DateTime)

  def __init__(self, patient_id=1, caregiver_id=2, drug=None, consumption_interval=None, dosage=None, start_date=None, end_date=None):
    self.patient_id = patient_id
    self.caregiver_id = caregiver_id
    self.drug = drug
    self.consumption_interval = consumption_interval
    self.dosage = dosage
    self.start_date = start_date
    self.end_date = end_date

class DrugInventory(db.Model):
  __tablename__ = 'drug_inventory'
  id = db.Column(db.Integer, primary_key=True)
  prescription_id = db.Column(db.Integer, db.ForeignKey('prescription.id'), index=True)
  inventory = db.Column(db.Integer)
  time_stamp = db.Column(db.DateTime)

  def __init__(self, prescription_id, inventory, date):
    self.prescription_id = prescription_id
    self.inventory = inventory
    self.time_stamp = date

class MachineUsers(db.Model):
  __tablename__ = 'machine_users'
  id = db.Column(db.Integer, primary_key=True)
  machine_id = db.Column(db.String(64), index=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  __table_args__ = (db.UniqueConstraint('machine_id', 'user_id'),)

  def __init__(self, machine_id, user_id):
    self.machine_id = machine_id
    self.user_id = user_id

"""
Transforms a model into a dictionary which can be dumped to JSON.
"""
def serialize(model):
  columns = [c.key for c in class_mapper(model.__class__).columns]
  return dict((c, getattr(model, c)) for c in columns)

def custom_parser(obj):
  if isinstance(obj, datetime.datetime):
    if obj.utcoffset() is not None:
      obj = obj - obj.utcoffset()
#  return '%s/%s/%s' % (obj.year, obj.month, obj.day)
  return time.mktime(obj.timetuple())
