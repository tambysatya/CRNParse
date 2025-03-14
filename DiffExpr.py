
import libsbml
from utils import parse_expr
import sympy

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

        for paramindex, param in enumerate(sbml_mdl.getListOfParameters()):
            self.parameters[param.getId()] = Parameter(paramindex, param)
            paramindex += 1

        specieindex, paramindex = 0,0
        for specie in sbml_mdl.getListOfSpecies():
            if specie.getBoundaryCondition() or specie.getConstant():
                s = Specie(paramindex, specie, isParam=True)
                self.parametersspecies[specie.getId()] = s
                paramindex += 1
            else:
                s = Specie(specieindex, specie, isParam=False)
                self.species[specie.getId()] = s
                specieindex += 1


        for index, reaction in enumerate(sbml_mdl.getListOfReactions()):
            reactionid=reaction.getId()
            self.reactions[reactionid]=Reaction(index, reaction)
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
        species_symbol_map = map(lambda specie: (sympy.symbols(specie.internal.getId()), specie.symbol),
                                 self.species.values())
        paramspecies_symbol_map = map(lambda specie: (sympy.symbols(specie.internal.getId()), specie.symbol),
                                      self.parametersspecies.values())
        param_symbol_map = map(lambda param: (sympy.symbols(param.internal.getId()), param.symbol),
                                 self.parameters.values())

        symbol_map = dict(species_symbol_map) | dict(paramspecies_symbol_map) | dict(param_symbol_map)



        substituted = True
        #iteratively simplifies and substitutes variables that have been proved to be constant
        while (substituted == True):
            print ("substituting...")
            substituted = False
            newspecies = {}
            for specieid, specie in self.species.items():
                expr = specie.buildDifferentialEquation(self.reactions)
                #expr = expr.subs(symbol_map)
                expr = self.expandFunctions(expr)
                if expr == 0:
                    newspecie = Specie (len(self.parametersspecies),specie.internal, isParam=True)
                    self.parametersspecies[specieid] = newspecie
                    print (f"{specieid} is constant and thus becomes the parameter {newspecie.symbol}")
                    substituted=True
                else:
                    newspecies[specieid] = specie
                    self.eqdiffsystem[specieid] = expr
                    print (f"{specie.internal.getId()}|{specie.symbol}: ", expr)
            self.species = newspecies

    def rlabelSymbols(self):
        """
            Labels species "x1...xN" and parameters "k1...kN"
        """
        speciesym = {}
        specieidx, paramidx = 0,0
        for paramid in [param.getId() for param in self.mdl.getListOfLocalParameters()]: #required to keep the order identical as described in the sbml file
            self.parameters[paramid].reindex(paramidx)
            paramidx += 1
        for specieid in [specie.getId() for specie in self.mdl.getListOfSpecies()]:
            if specieid in self.species:
                self.species[specieid].reindex(specieidx)
                specieidx += 1
            else:
                self.parametersspecies[specieid].reindex(paramidx)
                paramidx += 1
        for reactionid in [reaction.getId() for reaction in self.mdl.getListOfReactions()]:
            reaction = self.reactions[reactionid]
        

    def expandFunctions(self, expression):
        while True: #because there is no infinite recursions in python (nor do-until syntax) -_-
            recursive_call = False
            for func in expression.atoms(sympy.Function):
                name = func.func.__name__
                if name in self.functions:
                    expression = self.functions[name].apply(expression)
                    recursive_call = True
            if recursive_call == False:
                break
        return expression
            




def test():
    system = DiffEqSystem(mdl)
    return system

mdl = libsbml.readSBML("examples/BIOMD0000000056_decomposition_r1.xml").getModel()
#mdl = libsbml.readSBML("examples/BIOMD0000000095_decomposition_r1.xml").getModel()
#mdl = libsbml.readSBML("examples/BIOMD0000000096_decomposition_r1.xml").getModel()
#mdl = libsbml.readSBML("example1.xml").getModel()
