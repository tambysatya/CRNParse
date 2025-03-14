

import libsbml
from utils import parse_expr
import sympy


t = sympy.symbols("t")


class Specie ():
    def __init__ (self, specie, reactionids = set()):
        self.reactions = reactionids #the reaction IDs where the considered specie is either a product or reactant
        self.internal = specie #the sbml specie object
        self.symbol = sympy.Dummy()

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
    
