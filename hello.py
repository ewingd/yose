import os
from flask import Flask
from flask import Response
from flask import render_template
from flask import request

app = Flask(__name__)
app.debug = True

@app.route('/')
def hello():
    return render_template('hello.html')

@app.route('/ping')
def ping():
    return Response('{ "alive" : true }', mimetype='application/json')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/primefactors')
def prime_factors():
    number = int(request.args.get('number'))
    factors = get_prime_factors(number)
    json = '{"number" : %s, "decomposition" : %s}' % (str(number), factors)
    return Response(json, mimetype='application/json')


def get_prime_factors(number):
    return [2] * (number / 2)
