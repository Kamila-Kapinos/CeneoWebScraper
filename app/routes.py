from unicodedata import name
from app import app
from flask import render_template

@app.route('/')
@app.route('/index/<name>')
def index(name='Hello world!!'):
    return render_template('index.html.jinja', text=name)



