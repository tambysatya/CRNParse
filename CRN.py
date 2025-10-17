from utils import *

import libsbml
import tellurium as te

class CRN (libsbml.Model):
    def __init__(self, fname, verbose=False):
        sbml = libsbml.readSBML(fname).getModel() 
        if not sbml:
            raise ValueError ("Invalid file "+ fname+". Check if the file exists.")
        super().__init__(sbml)

        self.tellurium = loadModel(fname)
        self.odes_expr = parseEquations(te.getODEsFromModel(self.tellurium), verbose=verbose)
        self.classifySymbols()


    def classifySymbols (self):
        """
            Classifies the symbols according to the type of entity they refer to
        """
        if self.odes_expr == None:
            raise ValueError ("self.odes_expr is None.")
        unord_independent_species = self.tellurium.getIndependentFloatingSpeciesIds() #might not follow the order of the SBML
        all_symbols = set()
        symSpecies, symParams, symCompartments = [], [], []
        symConstantSpecies = [] #constant species
        symLocalParams = [] #local parameters

        for term, eq in self.odes_expr.items():
            all_symbols.add(term)
            all_symbols = all_symbols.union(eq.atoms(sp.Symbol))

        for s in self.getListOfSpecies():
            sym = sp.Symbol(sanitize_expr(s.getId()))
            if sym in all_symbols:
                symSpecies.append(sym)
                all_symbols.remove(sym)
            else:
                symConstantSpecies.append(sym)

        for c in self.tellurium.getCompartmentIds():
            sym = sp.Symbol(sanitize_expr(c))
            if sym in all_symbols:
                symCompartments.append(sym)
                all_symbols.remove(sym)

        for p in self.getListOfParameters():
            sym = sp.Symbol(sanitize_expr(p.getId()))
            if sym in all_symbols:
                symParams.append(sym)
                all_symbols.remove(sym)

        for r in self.getListOfReactions():
            r_name = r.getId()
            l = r.getKineticLaw()
            for p in l.getListOfParameters():
                sym = sp.Symbol(sanitize_expr(r_name + "_" + p.getId()))
                if sym in all_symbols:
                    symLocalParams.append(sym)
                    all_symbols.remove(sym)
            #required depending on the SBML version
            for p in l.getListOfLocalParameters():
                sym = sp.Symbol(sanitize_expr(r_name + "_" + p.getId()))
                if sym in all_symbols:
                    symLocalParams.append(sym)
                    all_symbols.remove(sym)
            

        if all_symbols != set():
            #print ("Not all symbols have been extracted: ", all_symbols)
            raise ValueError ("Not all symbols have been extracted: ", all_symbols)
        self.symSpecies, self.symParams, self.symCompartments = symSpecies, symParams, symCompartments
        self.symConstantSpecies = symConstantSpecies
        self.symLocalParams = symLocalParams


    def prettyODEs(self):
        """
            Display the ODEs nicely, where species and parameters are referred to as x1..xN and k1...kP respectively
        """
        return pprintEqs(self.rewriteODEs())


    def rewriteODEs (self):
        """
            Returns the ODE system where the symbols are relabelled using canonic names x1...xN and k1...kP
        """

        subs_dict = {}
        for i,sym in enumerate(self.symSpecies, 1):
            subs_dict[sym] = sp.Symbol("x"+str(i))
        
        k = 1

            
        for sym in self.symParams:
            subs_dict[sym] = sp.Symbol("k"+str(k))
            k+= 1
        for sym in self.symCompartments:
            subs_dict[sym] = sp.Symbol("k"+str(k))
            k+= 1

        for sym in self.symLocalParams:
            subs_dict[sym] = sp.Symbol("k"+str(k))
            k+= 1

        for sym in self.symConstantSpecies:
            subs_dict[sym] = sp.Symbol("k"+str(k))
            k+= 1

        odes = self.odes_expr.copy()
        odes = rewriteODEs(odes, subs_dict)

        return odes






