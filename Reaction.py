

import sympy

import libsbml
from Specie import *
from Parameter import *

class Reaction():
    def __init__ (self,index,reaction):
        self.index = index
        self.internal = reaction
        self.localparameters = {}
        self.kineticformula = parse_expr(reaction.getKineticLaw().getFormula())
        for paramindex, param in enumerate(reaction.getKineticLaw().getListOfLocalParameters()):
            paramname = f"L{index}_{paramindex}"
            self.localparameters[param.getId()] = Parameter(paramindex, param, name=paramname)
            self.kineticformula = self.kineticformula.subs(param.getId(),sympy.symbols(paramname) )
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


