

import sympy

import libsbml
from Specie import *
from Parameter import *

class Reaction():
    def __init__ (self,reaction):
        self.internal = reaction
        self.localparameters = {}
        self.kineticformula = parse_expr(reaction.getKineticLaw().getMath())
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
    
    def rewriteKineticFormula(self, speciessymb, globalparamssymb, paramspeciessymb, reactionlocalparamssymb, symbolmap):
        #paramsub = [(param.internal.getId(), param.symbol()) in self.localparameters]
        print ("rewriting ", self.internal.getId())
        expr = parse_expr(self.internal.getKineticLaw().getMath())
        
        expr = expr.subs(reactionlocalparamssymb[self.internal.getId()]) #first rewrite the local params (that shadows the global params)
        expr = expr.subs(speciessymb | globalparamssymb | paramspeciessymb)

        expr = expr.subs(symbolmap)

        #expr = expr.subs(paramsub)
        self.kineticformula = expr
        return expr


