import os
from flask import Flask
from flask import Response
from flask import render_template
from flask import request

from collections import OrderedDict

import json

app = Flask(__name__)
app.debug = True

def to_roman(numbers):
    output = []
    values = OrderedDict([('C', 100),
                          ('XC', 90),
                          ('L', 50),
                          ('XL', 40),
                          ('X', 10),
                          ('IX', 9),
                          ('V', 5),
                          ('IV', 4),
                          ('I', 1)])


    for number in numbers:
        s = ''
        for k, v in values.iteritems():
            while number >= v:
                number -= v
                s = s + k
        output.append(s)

    return output

def from_roman(number):
    t = type(number).__name__
    if t != 'str' and t != 'unicode':
        raise ValueError('Not a valid roman numeral')

    output = 0
    values = OrderedDict([('C', 100),
                          ('XC', 90),
                          ('L', 50),
                          ('XL', 40),
                          ('X', 10),
                          ('IX', 9),
                          ('V', 5),
                          ('IV', 4),
                          ('I', 1)])
    while number:
        orig_number = number
        for k, v in values.iteritems():
            if number.startswith(k):
                output += v
                number = number[len(k):]
        if orig_number == number:
            raise ValueError('Not a valid roman numeral')
    return output

def romanize(function):
    def wrapper(number):
        try:
            dec_number = from_roman(number)
            result = function(dec_number)
            result = to_roman(result)
        except ValueError:
            result = function(number)
        return result
    return wrapper

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
        number = map(str, number.split(','))
        number = map(str.strip, number)
        result = process_prime_factors(number)
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
            factors = get_prime_factors(number)
            output = {"number" : number, "decomposition" : factors}
        except ValueError, e:
            output = {"number" : number, "error" : "%s" % (e.message)}
        result.append(output)
    return result

@romanize
def get_prime_factors(number):
    try:
        number = int(number)
    except ValueError:
        raise ValueError("not a number")

    if number > 1000000:
        raise ValueError("too big number (>1e6)")
    elif number < 2:
        raise ValueError("not an integer > 1")

    factors = []
    current_number = 2

    while number != 1:
        if number % current_number == 0:
            factors.append(current_number)
            number = number / current_number
        else:
            current_number += 1
    return factors
