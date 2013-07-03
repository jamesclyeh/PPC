from app import db

class CareGiver(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(64), index = True, unique = True)
  email = db.Column(db.String(120), index = True, unique = True)

class Patient(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  nickname = db.Column(db.String(64), index = True, unique = True)
  email = db.Column(db.String(120), index = True, unique = True)

  def __repr__(self):
    return '<User %r>' % (self.nickname)
