import os
from flask import Flask
from flask import Response
from flask import render_template
from flask import request

import json

from roman import romanize

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

@app.route('/minesweeper')
def minesweeper():
    return render_template('minesweeper.html')

@app.route('/fire/geek')
def fire_api():
    width = request.args.get('width')
    board = request.args.get('map')
    board = parse_board(str(board), int(width))
    moves = calculate_moves(board)
    result = {'map' :  board, 'moves' : moves}
    return Response(json.dumps(result), mimetype='application/json')

def parse_board(input_board, width):
    input_board = list(input_board)
    output_board = []
    while input_board:
        output_row = ''
        for _ in range(0, width):
            output_row = output_row + input_board.pop(0)
        output_board.append(output_row)
    return output_board

def calculate_moves(board):
    plane = find_char('P', board)
    water = find_char('W', board)
    fire = find_char('F', board)

    moves = calculate_segment(plane, water, avoid=fire)
    addl_moves = calculate_segment(water, fire)
    for move in addl_moves:
        moves.append(move)
    return moves

def calculate_segment(start, end, avoid=False):
    moves = []
    visited = []
    visited.append(start)
    visited.append(avoid)
    cur_y, cur_x = start
    while (cur_y, cur_x) != end:
        if cur_y < end[0] and (cur_y + 1, cur_x) not in visited:
            moves.append({'dx': 0, 'dy' : 1})
            cur_y += 1
        elif cur_y > end[0] and (cur_y - 1, cur_x) not in visited:
            moves.append({'dx': 0, 'dy' : -1})
            cur_y -= 1
        elif cur_x < end[1] and (cur_y, cur_x + 1) not in visited:
            moves.append({'dx': 1, 'dy' : 0})
            cur_x += 1
        elif cur_x > end[1] and (cur_y, cur_x - 1) not in visited:
            moves.append({'dx': -1, 'dy' : 0})
            cur_x -= 1
        else:
            # just pick a move without caring about the direction
            # the moves in the correct direction aren't possible
            if (cur_y + 1, cur_x) not in visited:
                moves.append({'dx': 0, 'dy': 1})
                cur_y += 1
            elif (cur_y - 1, cur_x) not in visited:
                moves.append({'dx': 0, 'dy' : -1})
                cur_y -= 1
            elif (cur_y, cur_x + 1) not in visited:
                moves.append({'dx': 1, 'dy' : 0})
                cur_x += 1
            elif (cur_y, cur_x - 1) not in visited:
                moves.append({'dx': -1, 'dy' : 0})
                cur_x -= 1
    return moves

def find_char(value, board):
    for key, row in enumerate(board):
        if value in row:
            return key, row.index(value)

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
