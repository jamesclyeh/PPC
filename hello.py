import os
from flask import Flask, render_template

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
    'postgresql+psycopg2://awvolathokychi:SfaeRpVGxZowm_K7IDkTGvEvcM' +
    '@ec2-23-23-95-222.compute-1.amazonaws.com' +
    ':5432/d6p5qsqchkuarn')

@app.route('/')
def hello():
  return 'Hello World'#render_template(app.root_path + '/static/form/form.html')
@app.route('/initDb')
def initDb():
  db = SQLAlchemy(app)
  return None
