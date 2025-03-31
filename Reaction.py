

import sympy as sp

import libsbml
from Specie import *
from Parameter import *
import numbers

class Reaction(libsbml.Reaction):
    def __init__ (self,reaction, functions={}):
        super().__init__(reaction)
        self.localparameters = {}
        law = reaction.getKineticLaw()
        if None == law:
            raise ValueError(f"reaction {reaction.getId()} does not have a kinetic law")
        self.kineticformula = parse_expr(law.getMath())
        localsymbs = {}
        #local parameters (depending on the version of the SBML)
        for param in reaction.getKineticLaw().getListOfLocalParameters(): #newer versions
            parameter = Parameter(param)
            self.localparameters[param.getId()] = parameter
            localsymbs[sp.Function(parameter.getId())()] = parameter.symbol
        for param in reaction.getKineticLaw().getListOfParameters(): #old versions
            parameter = Parameter(param)
            self.localparameters[param.getId()] = parameter
            localsymbs[sp.Function(parameter.getId())()] = parameter.symbol
        if not isinstance(self.kineticformula, numbers.Number):
            self.kineticformula = self.kineticformula.subs(localsymbs)
        self.expandFunctions(functions)

    def getStoichiometryMatrixCoeficient (self, specie):
        coef = 0
        specieid = specie.getId()
        for reactant in self.getListOfReactants():
            if reactant.getSpecies() == specieid:
                coef -= reactant.getStoichiometry()
        for product in self.getListOfProducts():
            if product.getSpecies() == specieid:
                coef += product.getStoichiometry()
        return coef
    def expandFunctions(self, functions):
        expression = self.kineticformula
        while True: #because there is no infinite recursions in python (nor do-until syntax) -_-
            recursive_call = False
            for func in expression.atoms(sp.Function):
                name = func.func.__name__
                if name in functions:
                    expression = functions[name].apply(expression)
                    recursive_call = True
            if recursive_call == False:
                break
        self.kineticformula = expression


