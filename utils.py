
import tellurium as te
import sympy as sp
import sympy2jax

import libsbml



forbidden_string = {"lambda":"λ"}
greek_dict = {
    'alpha': 'α', 'beta': 'β', 'gamma': 'γ', 'delta': 'δ',
    'epsilon': 'ε', 'zeta': 'ζ', 'eta': 'η', 'theta': 'θ',
    'iota': 'ι', 'kappa': 'κ', 'lambda': 'λ', 'mu': 'μ',
    'nu': 'ν', 'xi': 'ξ', 'pi': 'π', 'rho': 'ρ', 'sigma': 'σ',
    'tau': 'τ', 'upsilon': 'υ', 'phi': 'φ', 'chi': 'χ',
    'psi': 'ψ', 'omega': 'ω'
}


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

    for s, fix in greek_dict.items():
        fixed_string = fixed_string.replace(s, fix)
    return fixed_string
        
    

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
            if term[0] == 'd' and term[-3:] == "/dt":
                try:
                    term = term[1:-3]
                    diff_eqs[sp.Symbol(term)] = sp.parse_expr(eq)
                    #diff_eqs[sp.Symbol(term)] = sp.parse_expr(eq, evaluate=False)
                except IndexError as e:
                    if verbose:
                        print ("\t[!]:",e," =>  defaulting to 0")
                    diff_eqs[sp.Symbol(term)] = sp.parse_expr("0")
            else:
                intermediary_terms[sp.Symbol(term)] = sp.parse_expr(eq)
                #intermediary_terms[sp.Symbol(term)] = sp.parse_expr(eq, evaluate=False)
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
    







        


