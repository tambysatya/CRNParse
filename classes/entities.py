
import libsbml as sbml
from classes.expressions import *
import networkx as nx
from utils import *

import logging
logger = logging.getLogger(__name__)




class Specie(sbml.Species):
    def __init__(self, s):
        super().__init__(s)
        self.sym = sp.Symbol(s.getId())
        self.sym_compartment = sp.Symbol(s.getCompartment())

    def isConcentration(self):
        hasOnlySubstanceUnits = self.getHasOnlySubstanceUnits()
        if self.isSetHasOnlySubstanceUnits():
            return not hasOnlySubstanceUnits
        else:
            logger.warning(f"{self.sym}: hasOnlySubstanceUnits() not set TODO")
            return True
    def isConstant(self):
        constant = self.isSetConstant() and self.getConstant()
        boundary = self.isSetBoundaryCondition and self.getBoundaryCondition()
        return constant or boundary



class Reaction (sbml.Reaction, Expression):
    def __init__ (self, reaction, funcs=[], assignment_rules={}, species={}):
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
        for p in kinetic_law.getListOfParameters(): #for old versions
            name = p.getIdAttribute()
            new_name = reaction_id + "_" + name
            local_params[sp.Symbol(name)] = new_name
        

        
        self.rewrite(local_params)
        self.local_params = local_params

        self.applyAssignments(assignment_rules)
        self.applyFunctions(funcs)

        self.rewriteSubstanceInputs(species)

    def __str__ (self):
        return Expression.__str__(self)
    def __repr__(self):
        return self.__str__()

    def rewriteSubstanceInputs(self, species):
        """
            If described as f(...,Xj,...), rewrites it as f(...,xjVj,...)
        """
        subs = {s.sym:s.sym*s.sym_compartment for s in species.values() if not s.isConcentration() }
        if subs != {}:
            logger.info(f"{self.getId()}: Conversion between quantity to concentration for species {subs.keys()} in {self.expr}")
            self.rewrite(subs)



    def applyAssignments(self, assignment_rules): #TODO can it be done better (maybe the comparison, or processing the expressions of the assignments) ?
        """
            Applies the assignement multiple times
            Can be avoided if an assignment rule cannot involve others assignment rules
        """
        expr = self.expr.subs(assignment_rules)
        while expr != self.expr:
            self.expr = expr
            expr = self.expr.subs(assignment_rules)

    def applyFunctions(self, funcs):
        for f in funcs:
            self.expr = f.apply(self.expr)

        


class CRN():
    def __init__(self, mdl):
        self.mdl = mdl #to avoid garbage collection

        self.crn = nx.DiGraph()
        self.species = {} #correspondance id => specie object
        self.reactions = {}#correspondance id => reaction object
        self.functions = []
        self.assignment_rules = {} #assignments rules are substitutions

        logger.debug("Functions:")
        for f in mdl.getListOfFunctionDefinitions():
            fun = FunctionDefinition(f)
            self.functions.append(fun)
            logger.debug ("\t",fun)

        logger.debug("Rules:")
        for r in mdl.getListOfRules():
            if r.isAssignment():
                rule = AssignmentRule(r, self.functions)
                logger.debug("\tAssignment:",rule.name,"=",rule.expr)
                self.assignment_rules[rule.name] = rule.expr
     

        for s in mdl.getListOfSpecies():
            self.addSpecie(s)
        for r in mdl.getListOfReactions():
            self.addReaction(r)

    def addSpecie(self, specie):
        specie_id = specie.getId()
        self.species[specie_id] = Specie(specie)
        self.crn.add_node(specie_id)

    def addReaction(self,r):
        reaction_id = r.getId()
        self.reactions[reaction_id] = Reaction(r,
                                               funcs=self.functions,
                                               assignment_rules=self.assignment_rules,
                                               species=self.species)
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
        return [self.reactions[r] for r in self.crn.predecessors(s.getId())]

    def stoichio (self, nodeA, nodeB):
        return self.crn[nodeA.getId()][nodeB.getId()]["stoichiometry"]

    def getSpecieODE(self, s):
        rCons = self.isReactantOf(s) 
        rProd = self.isProductOf(s)
        expr = 0
        for r in rCons: #s is a reactant
            expr -= r.expr*self.stoichio(s,r)/s.sym_compartment
        for r in rProd: #s is a product
            expr += r.expr*self.stoichio(r,s)/s.sym_compartment
        return expr

    def getODEs(self, relabel=False,mappings=False):
        odes = {s.sym:self.getSpecieODE(s) for s in self.species.values()}
        if not relabel:
            return {k:v for k,v in odes.items() if v != 0}

        const_species = [s for s in self.species.values() if s.isConstant() or odes[s.sym] == 0]
        species = [s for s in self.species.values() if not (s.isConstant() or odes[s.sym] == 0)]
        
        subs = {}
        for i,s in enumerate(species,1):
            subs[s.sym] = sp.Symbol(f"x_{i}")
        k = 1
        for e in self.mdl.getListOfParameters():
            subs[sp.Symbol(e.getId())] = sp.Symbol(f"k_{k}")
            k+= 1
        for e in const_species:
            subs[sp.Symbol(e.getId())] = sp.Symbol(f"k_{k}")
            k+= 1
        for e in self.mdl.getListOfCompartments():
            subs[sp.Symbol(e.getId())] = sp.Symbol(f"k_{k}")
            k+= 1
        for e in [param for r in self.reactions.values() for param in r.local_params.values()]:
            subs[sp.Symbol(e)] = sp.Symbol(f"k_{k}")
            k+= 1

#        for specie_id, ode in odes.items():
#            if ode == 0:
#                continue
#            if ode.is_real:
#                ret[subs[specie_id]] = ode
#            else:
#                ret[subs[specie_id]] = ode.subs(subs)
#        return ret


        species_id = [s.sym for s in species]
        ret = {subs[specie_id]:odes[specie_id].subs(subs) for specie_id in species_id if odes[specie_id] != 0}
        if not mappings:
            return ret
        else:
            return ret, subs
        












        




