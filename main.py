
from classes.Expression import *
import libsbml as sbml


path= "/home/tamby/git/biomodels/biomodels/BIOMD0000000162.xml"

def getModel():
    return sbml.readSBML(path).getModel()


def readKineticLaws(name=None):
    if name == None:
        name = path
    mdl = sbml.readSBML(path).getModel()

    print ("REACTIONS:")
    for r in mdl.getListOfReactions():
        r_name = r.getId()
        expr = KineticLaw(r_name, r.getKineticLaw())
        print (r_name,"=",expr)

    print ("Rules:")
    for r in mdl.getListOfRules():
        if r.isAssignment():
            rule = AssignmentRule(r)
            print(rule)

