

import libsbml
from utils import parse_expr
import sympy


t = sympy.symbols("t")


class Specie ():
    def __init__ (self, index, specie, reactionids = set(), isParam=False):
        self.reactions = reactionids #the reaction IDs where the considered specie is either a product or reactant
        self.internal = specie #the sbml specie object
        self.index = index
        self.isParam = isParam
        if not isParam:
            self.symbol = sympy.Function("x"+str(index))(t)
        else:
            self.symbol = sympy.symbols("k"+str(index))
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
        #expr = expr_prefix + '+'.join(terms)
        return expr
    def reindex (self, idx):
        self.index = idx
        if self.isParam:
            self.symbol = sympy.symbols("k"+str(idx))
        else:
            self.symbol = sympy.symbols("x"+str(idx))


