# student number:
import re


def function_renamer(code):
    # 1. extract function name, with regex(Regular Expression)
    function_pattern = re.compile(r'.*def\s+(.+)\s*\(.+\)')
    names = function_pattern.findall(code)

    # 2. judge if it is camel
    if len(names) >0:
        d = to_dictionary(names)
        for name in names:
            # 3a. if camel, do nothing
            # 3b. if snake, snake_to_camel()
            new_camel_name = to_camel(name)
            # 4. replace snake name with camel name in code
            code = code.replace(name, new_camel_name)
    # 5. return result
    result = (d, code)
    return result


def is_camel(s):
    if '_' not in s:
        return True
    return False


def to_camel(snake_str):
    if is_camel(snake_str):
        return snake_str
    str.lower(snake_str)
    components = snake_str.split('_')
    # capitalize the first of each component except the first one
    # join them to string
    return components[0] + ''.join(x.title() for x in components[1:])


def to_dictionary(names):
    d = {}
    for name in names:
        d_function = {}
        if name:
            d_function['hash'] = hash(name)
            d_function['camelcase'] = to_camel(name)
            d_function['allcaps'] = str.upper(name)
            d[name] = d_function
    return d


### --- IMPORTANT: DO NOT REMOVE OR CHANGE THE CODE BELOW ---
if __name__ == '__main__':
    # Example 1
    testcases = {
        'example 1':
"""
def add_two_numbers(a, b):
  return a + b

print(add_two_numbers(10, 20))
""",
    'example 2' :
"""
def _major_split(*args):
  return (args[:2], args[2:])

def CheckTruth(t = True):
  print('t is', t)
  return _major_split([t]*10)

x, y = _major_split((10, 20, 30, 40, 50))
CheckTruth(len(x) == 10)
"""
    }
    for key, code in testcases.items():
        print(f'--- {key} ---')
        out = function_renamer(code)
        if not isinstance(out, tuple) or len(out)!=2:
            raise TypeError('function_renamer should return a tuple of length 2')
        d, newcode = out
        if not isinstance(d, dict):
            raise TypeError('return argument d should be a dictionary')
        if not isinstance(newcode, str):
            raise TypeError('return argument code should be a string')
        print('d = ', d)
        print('\ncode:')
        print(newcode)
