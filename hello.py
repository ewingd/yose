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

@app.route('/primeFactors')
def prime_factors():
    number = request.args.get('number')
    try:
        number = int(number)
        if number > 1000000:
            json = '{"number" : %s, "error" : "too big number (>1e6)"}' % (str(number))
        else:
            factors = get_prime_factors(number)
            json = '{"number" : %s, "decomposition" : %s}' % (str(number), factors)
    except ValueError:
        json = '{"number" : "%s", "error" : "not a number"}' % (str(number)) 

    return Response(json, mimetype='application/json')


def get_prime_factors(number):
    factors = []
    current_number = 2
    
    while number != 1:
        if number % current_number == 0:
            factors.append(current_number)
            number = number / current_number
        else:
            current_number += 1
    return factors
