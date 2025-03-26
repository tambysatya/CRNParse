

import libsbml
from utils import parse_expr
import sympy
import math



class Specie (libsbml.Species):
    def __init__ (self, specie, reactionids = set()):
        super().__init__(specie)
        self.reactions = reactionids #the reaction IDs where the considered specie is either a product or reactant
        self.symbol = sympy.Dummy()
        
        value = specie.getInitialConcentration()
        if math.isnan(value):
            self.initialvalue = specie.getInitialAmount()
        else:
            self.initialvalue = value

    def addReaction (self, reactionid):
        self.reactions.add(reactionid)
    def buildDifferentialEquation (self, reactions_dict):
        expr = 0
        for reactionid in self.reactions:
            reaction = reactions_dict[reactionid]
            kinetic = reaction.kineticformula
            coef = reaction.getStoichiometryMatrixCoeficient(self)
            if coef == 1:
                expr += kinetic
            elif coef == -1:
                expr -= kinetic
            else:
                expr += coef*kinetic
        return expr
    
