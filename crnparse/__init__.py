from crnparse.classes.entities import *

import libsbml



def parseSBML(filepath):
    mdl = libsbml.readSBML(filepath)
    if not mdl:
        raise ValueError (f"{filepath}: not found")
    sbml = mdl.getModel()
    return CRN(sbml)
    


