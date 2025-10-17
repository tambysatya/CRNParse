
import tellurium as te
import sympy as sp
import sympy2jax

import libsbml


forbidden_string = {"lambda":"λ"}


def loadModel (fname):
    mdl = te.loadSBMLModel(fname)
    mdl = te.loadAntimonyModel(mdl.getAntimony()) #to remove duplicates names in local parameters
    return mdl
def sanitize_expr (eq_string):

    fixed_string = eq_string

    #removing spaces
    fixed_string = fixed_string.replace(" ","")
    fixed_string = fixed_string.replace("\t","")

    for s, fix in forbidden_string.items():
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
                    diff_eqs[sp.Symbol(term)] = sp.parse_expr(eq, evaluate=False)
                except IndexError as e:
                    if verbose:
                        print ("\t[!]:",e," =>  defaulting to 0")
                    diff_eqs[sp.Symbol(term)] = sp.parse_expr("0")
            else:
                intermediary_terms[sp.Symbol(term)] = sp.parse_expr(eq, evaluate=False)
        except ValueError as e:
            if verbose: 
                print ("\t[!] skipping line: ", str(e))

    if verbose:
        print ("Rewriting intermediary terms: ", intermediary_terms)
    for term, eq in diff_eqs.items():
        diff_eqs[term] = eq.subs(intermediary_terms)

    return diff_eqs


def showEqs (diff_eqs):
    for term, eq in diff_eqs.items():
        print (term,"=", eq)




class CRNModel (libsbml.Model):
    def __init__(self, fname, verbose=False):
        sbml = libsbml.readSBML(fname).getModel() 
        if not sbml:
            raise ValueError ("Invalid file "+ fname+". Check if the file exists.")
        super().__init__(sbml)

        self.tellurium = loadModel(fname)
        self.odes_expr = parseEquations(te.getODEsFromModel(self.tellurium), verbose=verbose)
        self.extractSymbols()


    def extractSymbols (self):
        if self.odes_expr == None:
            raise ValueError ("self.odes_expr is None.")
        unord_independent_species = self.tellurium.getIndependentFloatingSpeciesIds() #might not follow the order of the SBML
        all_symbols = set()
        symSpecies, symParams, symCompartments = [], [], []

        for term, eq in self.odes_expr.items():
            all_symbols.add(term)
            all_symbols.union(eq.atoms(sp.Symbol))

        for s in self.getListOfSpecies():
            sym = sp.Symbol(s.getId())
            if sym in all_symbols:
                symSpecies.append(sym)
                all_symbols.remove(sym)

        for c in self.getListOfCompartments():
            sym = sp.Symbol(c.getId())
            if sym in all_symbols:
                symCompartments.append(sym)
                all_symbols.remove(sym)

        for p in self.getListOfParameters():
            sym = sp.Symbol(p.getId())
            if sym in all_symbols:
                symParams.append(sym)
                all_symbols.remove(sym)

        if all_symbols != set():
            raise ValueError ("Not all symbols have been extracted.")
        self.symSpecies, self.symParams, self.symCompartments = symSpecies, symParams, symCompartments







        


