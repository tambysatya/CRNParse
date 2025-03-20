import libsbml as l
import sympy as sp

def nodeToSym(ast):    
    match ast.getType():
        case AST_CONSTANT_E:
            return sp.exp(1)
        case AST_CONSTANT_FALSE	
            return sp.false
        case AST_CONSTANT_PI	
            return sp.pi
        case AST_CONSTANT_TRUE	
            return sp.true
        case AST_FUNCTION	
        case AST_FUNCTION_ABS	
        case AST_FUNCTION_ARCCOS	
        case AST_FUNCTION_ARCCOSH	
        case AST_FUNCTION_ARCCOT	
        case AST_FUNCTION_ARCCOTH	
        case AST_FUNCTION_ARCCSC	
        case AST_FUNCTION_ARCCSCH	
        case AST_FUNCTION_ARCSEC	
        case AST_FUNCTION_ARCSECH	
        case AST_FUNCTION_ARCSIN	
        case AST_FUNCTION_ARCSINH	
        case AST_FUNCTION_ARCTAN	
        case AST_FUNCTION_ARCTANH	
        case AST_FUNCTION_CEILING	
        case AST_FUNCTION_COS	
        case AST_FUNCTION_COSH	
        case AST_FUNCTION_COT	
        case AST_FUNCTION_COTH	
        case AST_FUNCTION_CSC
        case AST_FUNCTION_CSCH	
        case AST_FUNCTION_DELAY	
        case AST_FUNCTION_EXP	
        case AST_FUNCTION_FACTORIAL	
        case AST_FUNCTION_FLOOR	
        case AST_FUNCTION_LN	
        case AST_NAME
        case AST_FUNCTION_LOG	
        case AST_FUNCTION_MAX2	
        case AST_FUNCTION_MIN2	
        case AST_FUNCTION_PIECEWISE	
        case AST_FUNCTION_POWER	
        case AST_FUNCTION_QUOTIENT2	
        case AST_FUNCTION_RATE_OF2	
        case AST_FUNCTION_REM2	
        case AST_FUNCTION_ROOT	
        case AST_FUNCTION_SEC	
        case AST_FUNCTION_SECH	
        case AST_FUNCTION_SIN	
        case AST_FUNCTION_SINH	
        case AST_FUNCTION_TAN	
        case AST_FUNCTION_TANH	
        case AST_LAMBDA
        case AST_LOGICAL_AND
        case AST_LOGICAL_NOT
        case AST_LOGICAL_OR
        case AST_LOGICAL_XOR
        case AST_LOGICAL_IMPLIES2
        case AST_NAME_AVOGADRO1
        case AST_NAME_TIME
        case AST_ORIGINATES_IN_PACKAGE2

        case AST_RATIONAL
        case AST_INTEGER	
        case AST_REAL
        case AST_REAL_E

        case AST_RELATIONAL_EQ
        case AST_RELATIONAL_GEQ
        case AST_RELATIONAL_GT
        case AST_RELATIONAL_LEQ
        case AST_RELATIONAL_LT
        case AST_RELATIONAL_NEQ

        case AST_PLUS
        case AST_MINUS
        case AST_TIMES
        case AST_DIVIDE	
        case AST_POWER
        case AST_UNKNOWN

    pass
