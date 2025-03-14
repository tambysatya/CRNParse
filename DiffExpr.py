
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
                expr = self.expandFunctions(expr)
                if expr == 0:
                    self.parametersspecies[specieid] = specie
                    print (f"{specieid} is constant and thus becomes a parameter.")
                    substituted=True
                else:
                    newspecies[specieid] = specie
                    self.eqdiffsystem[specieid] = expr
            self.species = newspecies

        for specieid, expr in self.eqdiffsystem.items():
            print (specieid,": ", expr)

    def indexSymbols(self):
        """
            Labels species "x1...xN" and parameters "k1...kN"
        """

        # Constructions of the substitutions maps: ID -> Int (index)
        speciesidx = {}
        globalparamsidx = {}
        parametersspeciesidx = {}
        reactionlocalparametersidx = {} #map reactionid -> (map localparamID symbol)

        specieidx, paramidx = 0,0

        #global parameters
        for paramid in [param.getId() for param in self.mdl.getListOfParameters()]: #required to keep the order identical as described in the sbml file
            globalparamsidx[paramid] = paramidx
            paramidx += 1

        #species AND constant species
        for specieid in [specie.getId() for specie in self.mdl.getListOfSpecies()]:
            if specieid in self.species:
                speciesidx[specieid] = specieidx
                specieidx += 1
            else:
                parametersspeciesidx[specieid] = paramidx
                paramidx += 1

        #local parameters
        for reactionid in [reaction.getId() for reaction in self.mdl.getListOfReactions()]:
            reaction = self.reactions[reactionid]
            reactionlocalparametersidx[reaction] = {}
            for paramid in [param.getId() for param in reaction.internal.getKineticLaw().getListOfLocalParameters()]:
                reactionlocalparametersidx[reaction][paramid]=paramidx
                paramidx += 1
        

        

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
