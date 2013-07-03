from app import db

CARE_GIVER = 0
PATIENT = 1
class User(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(64), index = True, unique = True)
  role = db.Column(db.Integer)
  email = db.Column(db.String(120), unique = True)
  phone_number = db.Column(db.String(32))

  def __repr__(self):
    return '<User %r>' % (self.name)
