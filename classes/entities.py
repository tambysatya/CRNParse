
import libsbml as sbml
from classes.expressions import *




class Species(sbml.Species):
    def __init__(self, r):
        super().__init__(r)

class Reaction (sbml.Reaction, Expression):
    def __init__ (self, reaction, funcs=[], assignment_rules={}):
        """
            Instanciates a reactions and simplifies the kinetic law depending according to the set of functions and rules that are specified
        """
        reaction_id = reaction.getId()
        kinetic_law = reaction.getKineticLaw()

        sbml.Reaction.__init__(self, reaction)
        Expression.__init__(self, kinetic_law.getMath())


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

        




