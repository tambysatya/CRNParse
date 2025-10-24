
import libsbml as sbml
import sympy as sp
from sympy.core.expr import Expr
from sbml_expr_parse.read import parse_expr

import logging
logger = logging.getLogger(__name__)




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
        return str(self.name) + "=" + Expression.__str__(self)
    def __repr__(self):
        return self.__str__()
    def dict(self):
        return {self.name:self.expr}





class AssignmentRule (NamedExpression):
    def __init__(self, rule, funcs=[]):
        name = sp.Symbol(rule.getVariable())
        expr = rule.getMath()

        NamedExpression.__init__(self, name, expr)

        self.applyFunctions(funcs)

    def __str__(self):
        return NamedExpression.__str__(self)
    def __repr__(self):
        return self.__str__()
    def applyFunctions (self, funcs):
        for f in funcs:
            self.expr = f.apply(self.expr)





class FunctionDefinition(NamedExpression):
    def __init__(self, fun):
        """
        Note that there is no closure in SBML functions, so there is no need to apply other expressions
        "A further restriction on the content of 'math' is that it cannot contain references to variables other than the variables declared to the 'lambda' itself."
        """
        name = sp.Function(fun.getId())
        expr = fun.getMath()
        NamedExpression.__init__(self, name, expr)


    def __str__(self):
        return NamedExpression.__str__(self)
    def __repr__(self):
        return self.__str__()

    def apply (self, expr):
        """
            Evaluates the occurences of the function inside the specified expression
        """
        ret = expr
        for term in sp.preorder_traversal(expr):
            name = term.func
            if name == self.name:
                logger.debug(f"\trewriting {name} in {term}")
                args = term.args
                ret = ret.subs(term,self.expr(*args))
        return ret
            









        
        
