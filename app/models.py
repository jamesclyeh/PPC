from app import db

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

