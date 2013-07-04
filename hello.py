import json
import os

from app import models
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
    'postgresql+psycopg2://awvolathokychi:SfaeRpVGxZowm_K7IDkTGvEvcM' +
    '@ec2-23-23-95-222.compute-1.amazonaws.com' +
    ':5432/d6p5qsqchkuarn')

@app.route('/')
def hello():
  return 'Hello World'#render_template(app.root_path + '/static/form/form.html')

@app.route('/viewUsers')
def dbTest():
  users = models.User.query.all()
#  info_str = 'Num users: ' + str(len(users)) + '<br>'
#  info_str += '<br>Users:<br>'
#  info_str += '<br>'.join([user.name for user in users])
  return json.dumps({'Users': [models.serialize(user) for user in users]})
