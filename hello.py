import os
from flask import Flask
from flask import Response
from flask import render_template
from flask import request

import json

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
    numbers = request.args.getlist('number')
    result = []
    for number in numbers:
        try:
            number = int(number)
            if number > 1000000:
                output = {"number" : number, "error" : "too big number (>1e6)"}
            else:
                factors = get_prime_factors(number)
                output = {"number" : number, "decomposition" : factors}
        except ValueError:
            output = {"number" : number, "error" : "not a number"}
        result.append(output)

    # don't nest the results if only one
    if len(result) == 1:
        result = output

    return Response(json.dumps(result), mimetype='application/json')


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
