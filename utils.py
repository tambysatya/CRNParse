import sympy.parsing.sympy_parser as sp
from sympy.parsing.mathematica import parse_mathematica
from sympy import Dummy
from sympy.parsing.sympy_parser import auto_symbol, auto_number, factorial_notation


#from https://github.com/oradules/odeparse/blob/main/sympifyer.py
_escape_symbols = ( "E1","li", "Ei", "expint", "Shi", "Chi", "Ci", "sinc", "Li",  "E" ,"I", "S", "N",  "O", "Q", "Gt", "CC", "LC", "ff",
    "comp", "lcm", "gamma", "beta", "zeta", "LT", "GF", 
    "Si",
    "bin", "product", "def" )
#_escape_symbols = ( "E1", "E" ,"I", "S", "N", "C", "O", "Q", "Gt", "CC", "LC", "ff",
#    "comp", "lcm", "source", "gamma", "beta", "zeta", "LT", "GF", "def", "lambda", "as",
#    "Si" )


global_dict = {}
for s in _escape_symbols:
    global_dict[s] = Dummy()

def escapeSymbs (expr):
    for symb, dummy in global_dict.items():
        expr=expr.replace(symb, str(dummy))
    return expr



def parse_expr(expr):
    expr = expr.replace("^","**")
    expr = escapeSymbs(expr)
    print (expr)
    try:
        return sp.parse_expr(expr) #, global_dict=global_dict, transformations=(auto_symbol,auto_number,factorial_notation))
    except TypeError as err:
        print ("parse error for expression: ", expr)
        print (err)
        raise err
    except ValueError as err:
        print ("parse error for expression: ", expr)
        print (err)
        raise err
    except _ as err:
        print ("parse error for expression: ", expr)
        print (err)
        raise err
