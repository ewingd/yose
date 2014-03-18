import os
from flask import Flask
from flask import Response
from flask import render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('hello.html')

@app.route('/ping')
def ping():
    return Response('{ "alive" : true }', mimetype='application/json')

@app.route('/contact')
def contact():
    return render_template('contact.html')
