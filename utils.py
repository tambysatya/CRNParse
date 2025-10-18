
import tellurium as te
import sympy as sp
import sympy2jax

import libsbml
import builtins
import types
from sympy.functions.elementary.miscellaneous import Max, Min


forbidden_keys = ["E1", "CC", "S", "O", "Q", "EX", "N", "beta","gamma", "Lambda", "bin", "ff", "comp", "Product", "LC", "rad", "Gt", "Lt", "LT", "lcm", "maximum", "GF", "zeta", "Le", "Li", "Si", "deg"]


def getGlobalDict():
    global_dict = {}
    exec('from sympy import *', global_dict)

    builtins_dict = vars(builtins)
    for name, obj in builtins_dict.items():
        if isinstance(obj, types.BuiltinFunctionType):
            global_dict[name] = obj
    global_dict['max'] = Max
    global_dict['min'] = Min

    for key in forbidden_keys:
        del global_dict[key]



    return global_dict


global_dict = getGlobalDict()


def loadModel (fname):
    mdl = te.loadSBMLModel(fname)
    mdl = te.loadAntimonyModel(mdl.getAntimony()) #to remove duplicates names in local parameters
    return mdl
def sanitize_expr (eq_string):

    fixed_string = eq_string

    #removing spaces
    fixed_string = fixed_string.replace(" ","")
    fixed_string = fixed_string.replace("\t","")

    fixed_string = fixed_string.replace("()", "0")
    fixed_string = fixed_string.replace("lambda", "Lambda")
    fixed_string = fixed_string.replace("def", 'Def')
    fixed_string = fixed_string.replace("input", 'Input')
    fixed_string = fixed_string.replace("as", 'As')

    return fixed_string
        

def parse_expr(expr):
    return sp.parse_expr(expr, global_dict=global_dict)
    

def parseEquations (eq_string, verbose=False):
    eqs = eq_string.split("\n")
    diff_eqs = {}
    intermediary_terms = {}

    for line in eqs:
        try:
            if verbose:
                print (line)
            term, eq = line.split("=")
            term, eq = sanitize_expr(term), sanitize_expr(eq)
            if eq == '':
                if verbose:
                    print ("\t[!]:", term, "=",eq, " => defaultin to 0")
                eq = "0"
            if term[0] == 'd' and term[-3:] == "/dt":
                try:
                    term = term[1:-3]
                    diff_eqs[sp.Symbol(term)] = parse_expr(eq)
                    #diff_eqs[sp.Symbol(term)] = parse_expr(eq, evaluate=False)
                except IndexError as e:
                    if verbose:
                        print ("\t[!]:",e," =>  defaulting to 0")
                    diff_eqs[sp.Symbol(term)] = parse_expr("0")
            else:
                intermediary_terms[sp.Symbol(term)] = parse_expr(eq)
                #intermediary_terms[sp.Symbol(term)] = parse_expr(eq, evaluate=False)
        except ValueError as e:
            if verbose: 
                print ("\t[!] skipping line: ", str(e))

    if verbose:
        print ("Rewriting intermediary terms: ", intermediary_terms)
    for term, eq in diff_eqs.items():
        diff_eqs[term] = eq.subs(intermediary_terms)

    return diff_eqs


def pprintEqs (diff_eqs):
    expr = ""
    for term, eq in diff_eqs.items():
        expr += str(term) +"=" + str(eq) + "\n"
    return expr



def rewriteODEs (old_odes, subs_dict):
    """
        Rewrites the symbols of an ODEs system represented as a dictionnary dx:dt => f(x, theta)
    """
    odes = {}
    for term, eq in old_odes.items():
        rew_term = term.subs(subs_dict)
        rew_eq = eq.subs(subs_dict)
        odes[rew_term] = rew_eq
    return odes
    







        


