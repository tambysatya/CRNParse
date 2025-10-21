
from classes.expressions import *
from classes.entities import * 
import libsbml as sbml
import glob


path2= "/home/tamby/git/biomodels/biomodels/BIOMD0000000169.xml" #has functions
path= "/home/tamby/git/biomodels/biomodels/BIOMD0000000586.xml" #has functions and assignment rules
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
        expr = Reaction(r)
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


def parseModel(file=path):
    mdl = sbml.readSBML(path).getModel()

    print ("Parsing functions")
    funcs = []
    for f in mdl.getListOfFunctionDefinitions():
        fun = FunctionDefinition(f)
        funcs.append(fun)
        print ("\t",fun)

    assignment_rules = {} #ATTENTION assignment rules stored in a dictionnary
    print ("Parsing assignments...")
    for r in mdl.getListOfRules():
        if r.isAssignment():
            rule = AssignmentRule(r, funcs)
            print ("\t",rule)
            assignment_rules[rule.name] = rule.expr
            

    print ("Parsing reactions...")
    for r in mdl.getListOfReactions():
        r = Reaction(r, funcs=funcs, assignment_rules=assignment_rules)
        print ("\t",r.getId(),":", r.expr)



def findFunctionModel ():
    for f in filenames:
        mdl = sbml.readSBML(f).getModel()
        if len(list(mdl.getListOfFunctionDefinitions())) > 0 and len([r for r in mdl.getListOfRules() if r.isAssignment()]) > 0:
            return f
