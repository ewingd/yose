import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello Yose'

@app.route('/ping')
def ping():
    return '{ "alive" : true }'
