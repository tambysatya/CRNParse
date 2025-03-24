
import libsbml
from utils import parse_expr
import sympy as sp
import argparse

from astread import TIME_SYMBOL
from Specie import *
from Reaction import *
from Parameter import *
from Function import *



class DiffEqSystem ():

    def __init__(self, sbml_mdl):
        self.mdl = sbml_mdl
        self.reactions = {} # map reactionid -> Reaction
        self.species = {}   # map specieid -> Specie : for the variables species
        self.parametersspecies = {} #map specieid -> Specie : for the constant specices that acts like parameters
        self.parameters = {} #map identifier -> Parameter (global parameters)
        self.functions = {} # map functionID -> Function (for the functions defined in the sbml)
        self.eqdiffsystem = {} #specieid -> expression: system of differential equations
        

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
        print (f"Found {len(self.species)} species, {len(self.reactions)} reactions, {len(self.parameters)} parameters, {len(self.parametersspecies)} species considered as parameters and {len(self.functions)} function definitions.")
    
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
                    newspecies[specieid] = specie
                    self.eqdiffsystem[specieid] = expr
            self.species = newspecies

        for specieid, expr in self.eqdiffsystem.items():
            print (specieid,": ", expr)
        
        print ("rewriting:")
        self.rewriteSymbols()

       
    def rewriteSymbols(self):
        speciesDict = {sp.Function(sym.getId())():sp.Function(sym.symbol)(TIME_SYMBOL) for sym in self.species.values()}
        paramspeciesDict = {sp.Function(sym.getId())():sp.Function(sym.symbol)(TIME_SYMBOL) for sym in self.parametersspecies.values()}
        parameters = {sp.Function(sym.getId())():sym.symbol for sym in self.parameters.values()}
        for expr in self.eqdiffsystem:
            self.eqdiffsystem[expr] = (self.eqdiffsystem[expr].subs(speciesDict | paramspeciesDict |parameters))
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
        with open(filename, "w") as file:
            for var, eq in self.eqdiffsystem.items():
                file.write(f"{var}: {eq}\n")
            



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
