
import libsbml

import sympy as sp


class Compartment (libsbml.Compartment):
    def __init__(self,compartment):
        super().__init__(compartment)
        self.symbol = sp.Dummy()
