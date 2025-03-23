

import sympy

import libsbml
from Specie import *
from Parameter import *

class Reaction(libsbml.Reaction):
    def __init__ (self,reaction):
        super().__init__(reaction)
        self.localparameters = {}
        law = reaction.getKineticLaw()
        if None == law:
            raise ValueError(f"reaction {reaction.getId()} does not have a kinetic law")
        self.kineticformula = parse_expr(law.getMath())
        for param in reaction.getKineticLaw().getListOfLocalParameters():
            self.localparameters[param.getId()] = Parameter(param)
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
    
    def rewriteKineticFormula(self, speciessymb, globalparamssymb, paramspeciessymb, reactionlocalparamssymb, symbolmap):
        #paramsub = [(param.internal.getId(), param.symbol()) in self.localparameters]
        print ("rewriting ", self.internal.getId())
        expr = parse_expr(self.getKineticLaw().getMath())
        
        expr = expr.subs(reactionlocalparamssymb[self.getId()]) #first rewrite the local params (that shadows the global params)
        expr = expr.subs(speciessymb | globalparamssymb | paramspeciessymb)

        expr = expr.subs(symbolmap)

        #expr = expr.subs(paramsub)
        self.kineticformula = expr
        return expr


