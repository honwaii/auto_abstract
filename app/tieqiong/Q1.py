import re
import string


def do_arithmetic(x, y, *op: str) -> float:  # annotate the return type float, but no verification

    # declare return value
    res = None
    # valid numbers(integers or floats)
    if type(x) not in (int, float) or type(y) not in (int, float):
        print("Invalid Parameters")

    # Division by zero, return None
    if y == 0:
        return res
    # op not specified, '+'
    if len(op) > 1:
        return res
    if len(op) == 0:
        op = '+'
    if len(op) == 1:
        op = op[0]
    if op in ('', None):
        op = '+'
    # op out of 4 operations, print 'Unknown operation', return None
    # if op not in ('+', '-', '*', '/'):
    #     print('Unknown operation')
    #     return res
    # op: string, +, -, *, /, default 'add'
    if '+' == op:
        res = float(x + y)
    elif '-' == op:
        res = float(x - y)
    elif '*' == op:
        res = float(x * y)
    elif '/' == op:
        res = float(x / y)
    else:
        print('Unknown operation')
        return res
    # return type: float
    print(res, type(res))
    return res


# parameter, argument
# variable

def sum_of_digits(s: str) -> int:
    s = str(s)
    # filter non-digit characters
    fil = filter(str.isdigit, s)
    digits = "".join(fil)
    sum = 0
    for i in range(0, len(digits)):
        sum += int(digits[i])

    return sum


if __name__ == '__main__':
    # print(do_arithmetic(35, 8))
    print(sum_of_digits('18ab9tew155'))