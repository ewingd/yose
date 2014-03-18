import os
from flask import Flask
from flask import Response

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello Yose'

@app.route('/ping')
def ping():
    return Response('{ "alive" : true }', mimetype='application/json')
