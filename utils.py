
#utilities functions

import sympy as sp
from sbml_expr_parse.read import *


def getStoichiometry(specie_ref):
    """
        Extracts the expression (sbml 2) or the real number of the stoichiometry 
        of the specified specie (described as a SpecieReference)
    """
    if specie_ref.isSetStoichiometry():
        return specie_ref.getStoichiometry()
    elif specie_ref.isSetStoichiometryMath():
        return parse_expr(specie_ref.getStoichiometryMath().getMath())
    else:
        return 1

