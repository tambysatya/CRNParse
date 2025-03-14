import sympy.parsing.sympy_parser as sp


def parse_expr(expr):
    expr = expr.replace("^","**")
    return sp.parse_expr(expr)
