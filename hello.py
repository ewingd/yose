import os
from flask import Flask
from flask import Response
from flask import render_template
from flask import request

import json

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

@app.route('/primeFactors/ui', methods=['GET', 'POST'])
def prime_factors_ui():
    result = []
    if request.method == 'POST':
        number = request.form.get('number')
        result = process_prime_factors([number])
    return render_template('prime_factors.html', result=result)

@app.route('/primeFactors')
def prime_factors():
    numbers = request.args.getlist('number')

    result = process_prime_factors(numbers)

    # don't nest the results if only one
    if len(result) == 1:
        result = result.pop()

    return Response(json.dumps(result), mimetype='application/json')

def process_prime_factors(numbers):
    result = []
    for number in numbers:
        try:
            number = int(number)
            if number > 1000000:
                output = {"number" : number, "error" : "too big number (>1e6)"}
            elif number < 2:
                output = {"number" : number, "error" : "not an integer > 1"} 
            else:
                factors = get_prime_factors(number)
                output = {"number" : number, "decomposition" : factors}
        except ValueError:
            output = {"number" : number, "error" : "not a number"}
        result.append(output)
    return result

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
