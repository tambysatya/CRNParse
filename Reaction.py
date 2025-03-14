

import sympy

import libsbml
from Specie import *
from Parameter import *

class Reaction():
    def __init__ (self,reaction):
        self.internal = reaction
        self.localparameters = {}
        self.kineticformula = parse_expr(reaction.getKineticLaw().getFormula())
        for param in reaction.getKineticLaw().getListOfLocalParameters():
            self.localparameters[param.getId()] = Parameter(param)
    def getStoichiometryMatrixCoeficient (self, specie):
        coef = 0
        specieid = specie.internal.getId()
        for reactant in self.internal.getListOfReactants():
            if reactant.getSpecies() == specieid:
                coef -= reactant.getStoichiometry()
        for product in self.internal.getListOfProducts():
            if product.getSpecies() == specieid:
                coef += product.getStoichiometry()
        return coef
    
    def substituteKineticFormula(self):
        paramsub = [(param.internal.getId(), param.symbol()) in self.localparameters]
        expr = parse_expr(self.internal.getKineticLaw().getFormula())
        expr = expr.subs(paramsub)
        self.kineticformula = expr
        return expr


