
from classes.Expression import *
import libsbml as sbml
import glob


path= "/home/tamby/git/biomodels/biomodels/BIOMD0000000169.xml"
glob_path = "/home/tamby/git/biomodels/biomodels/BIOMD*.xml"

filenames = [file for file in glob.glob(glob_path)]



def getModel():
    return sbml.readSBML(path).getModel()


def readKineticLaws(name=None):
    if name == None:
        name = path
    mdl = sbml.readSBML(path).getModel()

    exprs = []
    funs = []
    print ("REACTIONS:")
    for r in mdl.getListOfReactions():
        r_name = r.getId()
        expr = KineticLaw(r_name, r.getKineticLaw())
        exprs.append(expr)
        #print (r_name,"=",expr)

    print ("Rules:")
    for r in mdl.getListOfRules():
        if r.isAssignment():
            rule = AssignmentRule(r)
            exprs.append(rule)
            print(rule)

    print ("Functions:")
    funs = []
    for f in mdl.getListOfFunctionDefinitions():
        fun = FunctionDefinition(f)
        funs.append(fun)
        #print (fun)

    print ("Applying functions:")
    for e in exprs:
        expr = e.expr
        print ("Processing ",e)
        for fun in funs:
            expr = fun.apply(expr)
        print ("\tfinal:",expr)



def findFunctionModel ():
    for f in filenames:
        mdl = sbml.readSBML(f).getModel()
        if len(list(mdl.getListOfFunctionDefinitions())) > 0:
            return f
