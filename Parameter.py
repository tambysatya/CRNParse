import sympy

import libsbml

class Parameter():
    def __init__ (self, index, parameter, name=""):
        self.index = index
        self.internal = parameter
        if name == "":
            self.symbol = sympy.symbols("k"+str(index))
        else:
            self.symbol = sympy.symbols(name)
    def reindex (self, idx):
        self.index = idx
        self.symbol = sympy.symbols("k"+str(idx))



