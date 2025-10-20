
import libsbml as sbml
import sympy as sp
from sympy.core.expr import Expr
from sbml_expr_parse.read import parse_expr



class Expression (sbml.ASTNode):
    def __init__(self, ast_node):
        sbml.ASTNode.__init__(self, ast_node)
        self.sympy = parse_expr(ast_node)

    def __str__(self):
        return self.sympy.__str__()
    def __repr__(self):
        return self.__str__()


class NamedExpression (Expression):
    def __init__(self, name, ast_node):
        super().__init__(ast_node)
        self.name = name

    def __str__ (self):
        return self.name + "=" + Expression.__str__(self)
    def __repr__(self):
        return self.__str__()




class KineticLaw (sbml.KineticLaw, Expression):
    def __init__ (self, kinetic_law):
        sbml.KineticLaw.__init__(self, kinetic_law)
        Expression.__init__(self, kinetic_law.getMath())
    def __str__ (self):
        return Expression.__str__(self)
    def __repr__(self):
        return self.__str__()






        
        
