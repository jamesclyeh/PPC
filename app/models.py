import json

from app import db
from sqlalchemy.orm import class_mapper

CARE_GIVER = 0
PATIENT = 1

class User(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(64), index = True, unique = True)
  role = db.Column(db.Integer)
  email = db.Column(db.String(120), unique = True)
  phone_number = db.Column(db.String(32))

  def __init__(self, name, role, email, phone_number):
    self.name = name
    self.role = role
    self.email = email
    self.phone_number = phone_number

"""
Transforms a model into a dictionary which can be dumped to JSON.
"""
def serialize(model):
  columns = [c.key for c in class_mapper(model.__class__).columns]
  return dict((c, getattr(model, c)) for c in columns)

