
import libsbml as l
import jax.numpy as jnp
import equinox
import AST_TYPES.types as dbg

def evaluate_ast(ast, param_vals, x_vals):
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
            #return ast.getReal()
        case l.AST_REAL_E:
            return lambda _, _: jnp.float32(ast.getValue())
            #return ast.getReal()
        case l.AST_RATIONAL:
            return lambda _, _: jnp.float32(ast.getValue())
            #return ast.getReal()
        case l.AST_NAME:
            name = ast.getName()
            if name in param_vals:
                return lambda _, _:param_vals[name]
            else:
                return lambda _, _:x_vals[name]
        case _:
            raise ValueError (f"{dbg[t]} not differentiable")



