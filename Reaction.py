

import sympy as sp

import libsbml
from Specie import *
from Parameter import *
import numbers

class Reaction(libsbml.Reaction):
    def __init__ (self,reaction):
        super().__init__(reaction)
        self.localparameters = {}
        law = reaction.getKineticLaw()
        if None == law:
            raise ValueError(f"reaction {reaction.getId()} does not have a kinetic law")
        self.kineticformula = parse_expr(law.getMath())
        localsymbs = {}
        for param in reaction.getKineticLaw().getListOfLocalParameters():
            parameter = Parameter(param)
            self.localparameters[param.getId()] = parameter
            localsymbs[sp.Function(parameter.getId())()] = parameter.symbol
        for param in reaction.getKineticLaw().getListOfParameters():
            parameter = Parameter(param)
            self.localparameters[param.getId()] = parameter
            localsymbs[sp.Function(parameter.getId())()] = parameter.symbol
        if not isinstance(self.kineticformula, numbers.Number):
            self.kineticformula = self.kineticformula.subs(localsymbs)
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
    

