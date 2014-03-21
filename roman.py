from collections import OrderedDict

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
