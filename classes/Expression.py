
import libsbml as sbml
import sympy as sp
from sympy.core.expr import Expr
from sbml_expr_parse.read import parse_expr



class Expression (sbml.ASTNode):
    def __init__(self, ast_node):
        sbml.ASTNode.__init__(self, ast_node)
        self.expr = parse_expr(ast_node)

    def __str__(self):
        return self.expr.__str__()
    def __repr__(self):
        return self.__str__()

    def rewrite (self, subs_dict):
        self.expr = self.expr.subs (subs_dict)


class NamedExpression (Expression):
    def __init__(self, name, ast_node):
        super().__init__(ast_node)
        self.name = name

    def __str__ (self):
        return self.name.__str__() + "=" + Expression.__str__(self)
    def __repr__(self):
        return self.__str__()
    def dict(self):
        return {self.name:self.expr}




class KineticLaw (sbml.KineticLaw, Expression):
    def __init__ (self, reaction_id, kinetic_law):
        sbml.KineticLaw.__init__(self, kinetic_law)
        Expression.__init__(self, kinetic_law.getMath())

        #renames local parameter param as reaction_param
        local_params = {}
        for p in self.getListOfLocalParameters():
            name = p.getIdAttribute()
            new_name = reaction_id + "_" + name
            local_params[sp.Symbol(name)] = new_name
        
        self.rewrite(local_params)

    def __str__ (self):
        return Expression.__str__(self)
    def __repr__(self):
        return self.__str__()


class AssignmentRule (NamedExpression):
    def __init__(self, rule):
        name = sp.Symbol(rule.getVariable())
        expr = rule.getMath()

        NamedExpression.__init__(self, name, expr)

    def __str__(self):
        return NamedExpression.__str__(self)
    def __repr__(self):
        return self.__str__()


class FunctionDefinition(NamedExpression):
    def __init__(self, fun):
        name = sp.Symbol(fun.getId())
        expr = fun.getMath()
        NamedExpression.__init__(self, name, expr)
    def __str__(self):
        return NamedExpression.__str__(self)
    def __repr__(self):
        return self.__str__()








        
        
