import os
from flask import Flask, render_template

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

@app.route('/')
def hello():
  return render_template(app.root_path + '/static/form/form.html')
@app.route('/initDb')
def initDb():
  db = SQLAlchemy(app)
