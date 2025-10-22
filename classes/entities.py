
import libsbml as sbml
from classes.expressions import *
import networkx as nx
from utils import *




class Species(sbml.Species):
    def __init__(self, s):
        super().__init__(s)
        self.sym = sp.Symbol(s.getId())
        self.compartment = sp.Symbol(s.getCompartment())

    def isConcentration(self):
        hasOnlySubstanceUnits = self.getHasOnlySubstanceUnits()
        return not hasOnlySubstanceUnits



class Reaction (sbml.Reaction, Expression):
    def __init__ (self, reaction, funcs=[], assignment_rules={}):
        """
            Instanciates a reactions and simplifies the kinetic law depending according to the set of functions and rules that are specified
        """
        reaction_id = reaction.getId()
        kinetic_law = reaction.getKineticLaw()

        sbml.Reaction.__init__(self, reaction)
        Expression.__init__(self, kinetic_law.getMath())
        self.sym = sp.Symbol(reaction_id)


        #renames local parameter param as reaction_param
        local_params = {}
        for p in kinetic_law.getListOfLocalParameters():
            name = p.getIdAttribute()
            new_name = reaction_id + "_" + name
            local_params[sp.Symbol(name)] = new_name
        
        self.rewrite(local_params)
        self.local_params = local_params

        self.applyFunctions(funcs)
        self.expr = self.expr.subs(assignment_rules)

    def __str__ (self):
        return Expression.__str__(self)
    def __repr__(self):
        return self.__str__()
    def applyFunctions(self, funcs):
        for f in funcs:
            self.expr = f.apply(self.expr)

        


class CRN():
    def __init__(self, mdl):
        self.mdl = mdl #to avoid garbage collection

        self.crn = nx.DiGraph()
        self.species = {} #correspondance id => specie object
        self.reactions = {}#correspondance id => reaction object

        for s in mdl.getListOfSpecies():
            self.addSpecie(s)
        for r in mdl.getListOfReactions():
            self.addReaction(r)

    def addSpecie(self, specie):
        specie_id = specie.getId()
        self.species[specie_id] = specie
        self.crn.add_node(specie_id)

    def addReaction(self,r):
        reaction_id = r.getId()
        self.reactions[reaction_id] = r
        self.crn.add_node(reaction_id)
        for s in r.getListOfReactants():
            self.crn.add_edge(s.getSpecies(),reaction_id, stoichiometry=getStoichiometry(s))
        for s in r.getListOfProducts():
            self.crn.add_edge(reaction_id,s.getSpecies(), stoichiometry=getStoichiometry(s))
        for s in r.getListOfModifiers():
            self.crn.add_edge(s.getSpecies(),reaction_id, stoichiometry=0) #TODO

    def reactantsOf (self, r):
        return [self.species[p] for p in self.crn.predecessors(r.getId())]
    def productsOf (self, r):
        return [self.species[n] for n in self.crn.successors(r.getId())]

    def isReactantOf(self, s):
        """ List of reactions where s is a reactant"""
        return [self.reactions[r] for r in self.crn.successors(s.getId())]
    def isProductOf(self, s):
        """ List of reactions where s is a product """
        return [self.reactions[r] for r in self.crn.successors(s.getId())]
        return [self.reactions[r] for r in self.crn.predecessors(s.getId())]

    def stoichio (self, nodeA, nodeB):
        return self.crn[nodeA.getId()][nodeB.getId()]["stoichiometry"]

    def getSpecieODE(self, s, reactions_laws):
        rCons = self.isReactantOf(s) 
        rProd = self.isProductOf(s)
        expr = 0
        for r in rCons:
            expr += reactions_laws[r.getId]*self.stoichio(s,r)
        for r in rProd:
            expr += reactions_laws[r.getId]*self.stoichio(r,s)










        




