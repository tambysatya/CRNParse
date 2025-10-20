
from classes.Expression import *
import libsbml as sbml


path= "/home/tamby/git/biomodels/biomodels/BIOMD0000000289.xml"

def getModel():
    return sbml.readSBML(path).getModel()

