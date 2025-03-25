
import libsbml
from utils import parse_expr
import sympy as sp
import argparse

from astread import TIME_SYMBOL
from Compartment import *
from Specie import *
from Reaction import *
from Parameter import *
from Function import *



class DiffEqSystem ():

    def __init__(self, sbml_mdl):
        self.mdl = sbml_mdl
        self.compartments = {} # map compartmentid -> Compartment
        self.reactions = {} # map reactionid -> Reaction
        self.species = {}   # map specieid -> Specie : for the variables species
        self.parametersspecies = {} #map specieid -> Specie : for the constant specices that acts like parameters
        self.parameters = {} #map identifier -> Parameter (global parameters)
        self.functions = {} # map functionID -> Function (for the functions defined in the sbml)
        self.eqdiffsystem = {} #specieid -> expression: system of differential equations
        

        for compartment in sbml_mdl.getListOfCompartments():
            self.compartments[compartment.getId()] = Compartment(compartment)
        for function in sbml_mdl.getListOfFunctionDefinitions():
            self.functions[function.getId()] = Function(function)

        for param in sbml_mdl.getListOfParameters():
            self.parameters[param.getId()] = Parameter(param)

        for specie in sbml_mdl.getListOfSpecies():
            s = Specie(specie)
            if specie.getBoundaryCondition() or specie.getConstant():
                self.parametersspecies[specie.getId()] = s
            else:
                self.species[specie.getId()] = s


        for reaction in sbml_mdl.getListOfReactions():
            reactionid=reaction.getId()
            self.reactions[reactionid]=Reaction(reaction)
            for reactant in reaction.getListOfReactants():
                self.addReactionToSpecie(reactant.getSpecies(), reactionid)
            for product in reaction.getListOfProducts():
                self.addReactionToSpecie(product.getSpecies(), reactionid)
            for modifier in reaction.getListOfModifiers():
                self.addReactionToSpecie(modifier.getSpecies(), reactionid)
    
    def addReactionToSpecie (self, specieid, reactionid):
        try:
            self.species[specieid].addReaction(reactionid)
        except KeyError:
            if self.parametersspecies[specieid] != None:
                self.parametersspecies[specieid].addReaction(reactionid)
            else:
                raise KeyError(f"{specieid} in {reactionid} not registered in the list of species")

        
    def build (self):
        self.eqdiffsystem = {}

        substituted = True
        #iteratively simplifies and substitutes variables that have been proved to be constant
        while (substituted == True):
            substituted = False
            newspecies = {}
            for specieid, specie in self.species.items():
                expr = specie.buildDifferentialEquation(self.reactions)
                #expr = expr.subs(symbol_map)
                if expr == 0:
                    self.parametersspecies[specieid] = specie
                    print (f"{specieid} is constant and thus becomes a parameter.")
                    substituted=True
                elif expr.is_number:
                    self.eqdiffsystem[specieid] = expr
                else:
                    expr = self.expandFunctions(expr)

                    if expr == 0:
                        self.parametersspecies[specieid] = specie
                        print (f"{specieid} is constant and thus becomes a parameter.")
                    else:
                        newspecies[specieid] = specie
                        self.eqdiffsystem[specieid] = expr
            self.species = newspecies

        for specieid, expr in self.eqdiffsystem.items():
            print (specieid,": ", expr)
        
        print ("rewriting:")
        self.rewriteSymbols()

        print (f"Found {len(self.species)} species, {len(self.reactions)} reactions, {len(self.parameters)} parameters, {len(self.parametersspecies)} species considered as parameters and {len(self.functions)} function definitions.")

       
    def rewriteSymbols(self):
        """
        Rewrites the ODEs with unique symbols, in order to avoid shadowing declarations.
        Also converts the symbols (that are all constant functions) into time-dependent functions (for
        species) and constant symbols (for parameters)
        """
        compartmentsDict = {sp.Function(sym.getId())():sym.symbol for sym in self.compartments.values()}
        speciesDict = {sp.Function(sym.getId())():sp.Function(sym.symbol)(TIME_SYMBOL) for sym in self.species.values()}
        paramspeciesDict = {sp.Function(sym.getId())():sp.Function(sym.symbol)(TIME_SYMBOL) for sym in self.parametersspecies.values()}
        parameters = {sp.Function(sym.getId())():sym.symbol for sym in self.parameters.values()}
        for expr in self.eqdiffsystem:
            self.eqdiffsystem[expr] = (self.eqdiffsystem[expr].subs(compartmentsDict | speciesDict | paramspeciesDict |parameters))
            print ("\t",self.eqdiffsystem[expr])

        

    def expandFunctions(self, expression):
        while True: #because there is no infinite recursions in python (nor do-until syntax) -_-
            recursive_call = False
            for func in expression.atoms(sp.Function):
                name = func.func.__name__
                if name in self.functions:
                    expression = self.functions[name].apply(expression)
                    recursive_call = True
            if recursive_call == False:
                break
        return expression
    def writeDiffEqs (self, filename):
        symbolmap = {}
        count = 1
        for param in self.listParameters():
            symbolmap [param.symbol] = sp.symbols("k"+str(count))
            count += 1
        count =1
        for specie in self.species.values():
            symbolmap[sp.Function(specie.symbol)] = sp.Function("x"+str(count))
            count += 1

        with open(filename, "w") as file:
            for var, eq in self.eqdiffsystem.items():
                neq = eq.subs(symbolmap)
                neq = neq.subs(TIME_SYMBOL, sp.symbols("t")) #rewrite the time _t -> t
                file.write(f"{var}: {neq}\n")
            

    def listParameters (self):
        params = []
        
        for compartment in self.compartments.values():
            params.append(compartment)
        
        for param in self.parameters.values():
            params.append(param)

        for param in self.parametersspecies.values():
            params.append(param)

        for reaction in self.reactions.values():
            for param in reaction.localparameters.values():
                params.append(param)

        return params



def run(filename, targetname):
    mdl = libsbml.readSBML(filename).getModel()
    system = DiffEqSystem(mdl)
    system.build()
    system.writeDiffEqs(targetname)

def test():
    system = DiffEqSystem(mdl)
    system.build()
    return system



#mdl = libsbml.readSBML("examples/607.xml").getModel()

#mdl = libsbml.readSBML("examples/BIOMD0000000056_decomposition_r1.xml").getModel()
#mdl = libsbml.readSBML("examples/BIOMD0000000095_decomposition_r1.xml").getModel()
#mdl = libsbml.readSBML("examples/BIOMD0000000096_decomposition_r1.xml").getModel()
#mdl = libsbml.readSBML("example1.xml").getModel()
