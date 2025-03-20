import libsbml as l
import sympy as sp
import sympy.physics.units as u
from sympy.functions.elementary.complexes import *

TIME_SYMBOL = sp.Dummy()

def processLambda(ast):
    raise ValueError ("AST_LAMBDA not implemented")

def getFunctionSymb (ast):
        match ast.getType():
            case l.AST_FUNCTION:
                if ast.isOperator() or ast.isNumber():
                    raise ValueError ("getFunctionSymb(): type is AST_FUNCTION but ast.isOperator() or ast.isNumber()")
                return sp.Function(name)
            case l.AST_FUNCTION_ABS:
                return abs
            case l.AST_FUNCTION_ARCCOS:
                return sp.acos
            case l.AST_FUNCTION_ARCCOSH:
                return sp.acosh
            case l.AST_FUNCTION_ARCCOT:
                return sp.acot
            case l.AST_FUNCTION_ARCCOTH:
                return sp.acoth
            case l.AST_FUNCTION_ARCCSC:
                return sp.acsc
            case l.AST_FUNCTION_ARCCSCH:
                return sp.acsch
            case l.AST_FUNCTION_ARCSEC:
                return sp.asec
            case l.AST_FUNCTION_ARCSECH:
                return sp.asech
            case l.AST_FUNCTION_ARCSIN:
                return sp.asin
            case l.AST_FUNCTION_ARCSINH:
                return sp.asinh
            case l.AST_FUNCTION_ARCTAN:	
                return sp.atan
            case l.AST_FUNCTION_ARCTANH:
                return sp.atanh
            case l.AST_FUNCTION_CEILING:
                return sp.ceiling
            case l.AST_FUNCTION_COS:
                return sp.cos
            case l.AST_FUNCTION_COSH:
                return sp.cosh
            case l.AST_FUNCTION_COT:
                return sp.cot
            case l.AST_FUNCTION_COTH:
                return sp.coth
            case l.AST_FUNCTION_CSC:
                return sp.csc
            case l.AST_FUNCTION_CSCH:
                return sp.csch
            case l.AST_FUNCTION_FLOOR:
                return sp.floor
            case l.AST_FUNCTION_EXP:
                return sp.exp
            case l.AST_FUNCTION_FACTORIAL:
                return sp.factorial
            case l.AST_FUNCTION_LN:
                return sp.ln
            case l.AST_FUNCTION_LOG:
                return sp.log
            case l.AST_FUNCTION_SEC:
                return sp.sec
            case l.AST_FUNCTION_SECH:
                return sp.sech
            case l.AST_FUNCTION_SIN:
                return sp.sin
            case l.AST_FUNCTION_SINH:
                return sp.sinh
            case l.AST_FUNCTION_TAN:
                return sp.tan
            case l.AST_FUNCTION_TANH:
                return sp.tanh


            #calculus 
            case l.AST_FUNCTION_MAX2:
               return sp.Max
            case l.AST_FUNCTION_MIN2:
                return sp.Min

            case l.AST_FUNCTION_ROOT:
                return sp.root

            #polynomial quotients
            case l.AST_FUNCTION_QUOTIENT2:
                return sp.quo
            case l.AST_FUNCTION_REM2:
                return sp.rem


            case l.AST_FUNCTION_DELAY:	
                raise ValueError("AST_FUNCTION_DELAY not implemented")
            case l.AST_FUNCTION_PIECEWISE:	
                raise ValueError("AST_FUNCTION_PIECEWISE not implemented")
            case l.AST_FUNCTION_POWER:	
                raise ValueError("AST_FUNCTION_POWER not implemented")
            case l.AST_FUNCTION_RATE_OF2:	
                raise ValueError("AST_FUNCTION_RATE_OF2 not implemented")
            case l.AST_LAMBDA:
                return processLambda(ast)
            case l.AST_NAME:
                if ast.isOperator() or ast.isNumber():
                    raise ValueError ("getFunctionSymb(): type is AST_NAME but ast.isOperator() or ast.isNumber()")
                return sp.symbols(name)


def getConstantSymb (ast):
    match ast.getType():
        case l.AST_CONSTANT_FALSE:	
            return sp.false
        case l.AST_CONSTANT_TRUE:	
            return sp.true
        case l.AST_CONSTANT_E:
            return sp.exp(1)
        case l.AST_CONSTANT_PI:	
            return sp.pi
        case l.AST_NAME_AVOGADRO1:
            return u.avogadro_number
        case l.AST_INTEGER:	
            return ast.getValue()
        case l.AST_REAL:
            return ast.getValue()
            #return ast.getReal()
        case l.AST_REAL_E:
            return ast.getValue()
            #return ast.getReal()
        case l.AST_RATIONAL:
            return ast.getValue()
            #return ast.getReal()
        case l.AST_NAME_TIME:
            return TIME_SYMBOL

def getLogicalSymb (ast):
    match ast.getType():
        case l.AST_LOGICAL_AND:
            return sp.And
        case l.AST_LOGICAL_NOT:
            return sp.Not
        case l.AST_LOGICAL_OR:
            return sp.Or
        case l.AST_LOGICAL_XOR:
            return sp.Xor
        case l.AST_LOGICAL_IMPLIES2:
            return sp.Implies
def getRelationalSymb (ast):
    match ast.getType():
        case l.AST_RELATIONAL_EQ:
            return sp.Eq
        case l.AST_RELATIONAL_GEQ:
            return sp.Ge
        case l.AST_RELATIONAL_GT
            return sp.Gt
        case l.AST_RELATIONAL_LEQ
            return sp.Le
        case l.AST_RELATIONAL_LT
            return sp.Lt
        case l.AST_RELATIONAL_NEQ
            return sp.Ne

def getOperatorSymb (ast):
    match ast.getType():
        case l.AST_PLUS:
            return sp.Add
        case l.AST_TIMES:
            return sp.Mul
        case l.AST_POWER:
            return sp.Pow

        case l.AST_MINUS #TODO
        case l.AST_DIVIDE	



def processFunction (ast):
    symb = getFunctionSymb(ast)
    children = []
    for i in ast.getNumChildren():
        child = ast.getChild(i)
        expr = astToExpr(child)
        children.append(expr)
    return symb(*children)


def astToExpr(ast, symbolmap):    
    ast.canonicalize()
    if ast.isCiNumber():
        return processConstant(ast)
    elif ast.isFunction():
        return processFunction(ast)
    
        case l.AST_ORIGINATES_IN_PACKAGE2

        case l.AST_UNKNOWN

    pass
