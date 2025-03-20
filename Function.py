import libsbml
from utils import parse_expr
import sympy



class Function():
    def __init__(self, function):
        self.internal = function
        body = function.getBody()
        args = []
        for i in range(function.getNumArguments()):
            args.append(function.getArgument(i).getName())
        args = sympy.symbols(args)
        self.args = args
        self.name = function.getId()
        self.symbol = sympy.Function(self.name)(*args)


        self.expr = parse_expr(body)
        print (self.symbol,"=",body)

    def apply(self, expression):       
        for func in expression.atoms(sympy.Function):
            if func.func.__name__ == self.name:
                calledargs = func.args #the arguments on which the function is called
                symmap = dict(zip (self.args, calledargs))
                newexpr = self.expr.subs(symmap) #substitute the variables in the definition with the arguments of the function call
                expression = expression.subs(func, newexpr)
        return expression       


