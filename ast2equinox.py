
import libsbml as l
import jax
import jax.numpy as jnp
import jax.scipy as jsp
import equinox
import AST_TYPES.types as dbg

def ast_const (ast, params_names):
    t = ast.getType()
    match t:
        case l.AST_CONSTANT_E:
            return lambda _, _: jnp.exp(1)
        case l.AST_CONSTANT_PI:	
            return lambda _, _: jnp.pi
        case l.AST_NAME_AVOGADRO:
            return lambda _, _: jnp.float32(6.02214076e23)
        case l.AST_INTEGER:	
            return lambda _, _: jnp.float32(ast.getValue())
        case l.AST_REAL:
            return lambda _, _: jnp.float32(ast.getValue())
        case l.AST_REAL_E:
            return lambda _, _: jnp.float32(ast.getValue())
        case l.AST_RATIONAL:
            return lambda _, _: jnp.float32(ast.getValue())
        case l.AST_NAME:
            name = ast.getName()
            if name in params_names:
                return lambda param,_ : param_vals[name]
            else:
                return lambda _, x_vals: x_vals[name]
        case _:
            raise ValueError (f"{dbg[t]} not differentiable")


def ast_fun (ast, astfunctions, params_names):
        """
            Takes the list of function definitions astfunctions :: [params -> vals -> float]
            and the list of parameters names :: params_names :: Set String
            returns a differentiable function
        """
        match ast.getType():
            case l.AST_FUNCTION:
                if ast.isOperator() or ast.isNumber():
                    raise ValueError ("getFunctionSymb(): type is AST_FUNCTION but ast.isOperator() or ast.isNumber()")
                name = ast.getName()
                return astfunctions[name]
            case l.AST_FUNCTION_ABS:
                return jnp.abs
            case l.AST_FUNCTION_ARCCOS:
                return jnp.arccos
            case l.AST_FUNCTION_ARCCOSH:
                return jnp.arccosh
            case l.AST_FUNCTION_ARCSIN:
                return jnp.arcsin
            case l.AST_FUNCTION_ARCSINH:
                return jnp.arcsinh
            case l.AST_FUNCTION_ARCTAN:	
                return jnp.arctan
            case l.AST_FUNCTION_ARCTANH:
                return jnp.arctanh
            case l.AST_FUNCTION_CEILING:
                return jnp.ceil
            case l.AST_FUNCTION_COS:
                return jnp.cos
            case l.AST_FUNCTION_COSH:
                return jnp.cosh
            case l.AST_FUNCTION_FLOOR:
                return jnp.floor
            case l.AST_FUNCTION_EXP:
                return jnp.exp
            case l.AST_FUNCTION_FACTORIAL:
                return jsp.special.factorial
            case l.AST_FUNCTION_LN:
                return jnp.log
            case l.AST_FUNCTION_LOG:
                return jnp.log
            case l.AST_FUNCTION_SIN:
                return jnp.sin
            case l.AST_FUNCTION_SINH:
                return jnp.sinh
            case l.AST_FUNCTION_TAN:
                return jnp.tan
            case l.AST_FUNCTION_TANH:
                return jnp.tanh
            case l.AST_FUNCTION_MAX:
                nchildren = ast.getNumChildren()
                exprs = [read_ast(ast.getChild(i), astfunctions, params_names) for i in range(nchildren)]
                return lambda params,x_vals : jnp.max(jnp.stack([expr(params,x_vals) for expr in exprs]))
            case l.AST_FUNCTION_MIN:
                nchildren = ast.getNumChildren()
                exprs = [read_ast(ast.getChild(i), astfunctions, params_names) for i in range(nchildren)]
                return lambda params,x_vals : jnp.min(jnp.stack([expr(params,x_vals) for expr in exprs]))
            case l.AST_FUNCTION_ROOT:
                left = read_ast(ast.getLeftChild(),astfunctions, params_names)
                right = read_ast(ast.getRightChild(), astfunctions, params_names)
                return lambda params, x_vals: left(params, x_vals) ** (1/right(params,x_vals))

            case l.AST_FUNCTION_PIECEWISE:	
                return sp.Piecewise
            case l.AST_FUNCTION_POWER:	
                if ast.getNumChildren() > 2:
                    raise ValueError("AST_FUNCTION_POWER with args {ast.getNumChildren()} > 2")
                return sp.Pow
            case l.AST_FUNCTION_RATE_OF:	
                raise ValueError("AST_FUNCTION_RATE_OF not implemented")
            case l.AST_LAMBDA:
                return processLambda(ast)
            case l.AST_NAME:
                if ast.isOperator() or ast.isNumber():
                    raise ValueError ("getFunctionSymb(): type is AST_NAME but ast.isOperator() or ast.isNumber()")
                name = ast.getName()
                #if ast.getNumChildren() == 0:
                #    return sp.symbols(name)
                #else:
                return sp.Function(name)

            case _:
                raise ValueError (f"getType() {DBG.types[ast.getType()]} not implemented")


