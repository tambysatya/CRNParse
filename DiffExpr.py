
import libsbml
from sympy.parsing.sympy_parser import parse_expr
import sympy





class Specie ():
    def __init__ (self, index, specie, reactionids = set()):
        self.reactions = reactionids #the reaction IDs where the considered specie is either a product or reactant
        self.internal = specie #the sbml specie object
        self.index = index
        self.symbol = sympy.symbols("X"+str(index))

    def addReaction (self, reactionid):
        self.reactions.add(reactionid)
            
    def buildDifferentialEquation (self, reactions_dict):
        expr_prefix = "d"+self.internal.getId()+"/dt="
        terms = []
        for reactionid in self.reactions:
            reaction = reactions_dict[reactionid]
            kinetic = reaction.getKineticLaw().getFormula()
            coef = 0
            for reactant in reaction.getListOfReactants():
                if reactant.getSpecies() == self.internal.getId():
                    coef -= reactant.getStoichiometry()
                    break
            for product in reaction.getListOfProducts():
                if product.getSpecies() == self.internal.getId():
                    coef += product.getStoichiometry()
                    break
            if coef == 1:
                term = "(" + kinetic +")"
            elif coef == -1:
                term = "-(" + kinetic +")"
            else:
                term = str(coef)+'*('+kinetic+')'
            terms.append(term)
        #expr = expr_prefix + '+'.join(terms)
        expr = '+'.join(terms)
        return parse_expr(expr)
        
class Parameter():
    def __init__ (self, index, parameter):
        self.index = index
        self.internal = parameter
        self.symbol = sympy.symbols("K"+str(index))

class Function():
    def __init__(self, function):
        self.internal = function
        body = function.getBody()
        body = libsbml.formulaToL3String(body)
        args = []
        for i in range(function.getNumArguments()):
            args.append(function.getArgument(i).getName())
        args = sympy.symbols(args)
        self.name = function.getId()
        self.symbol = sympy.Function(self.name)(*args)


        body=body.replace("^","**") #TODO check the parsing 
        self.expr = parse_expr(body)

    def apply(self, expression):       
        for func in expression.atoms(sympy.Function):
            if func.func.__name__ == self.name:
                expression = expression.subs(func, self.expr)
        return expression       

class DiffEqSystem ():

    def __init__(self, sbml_mdl):
        self.reactions = {} # map reactionid -> sbml reaction object
        self.species = {}   # map specieid -> Specie : for the variables species
        self.parametersspecies = {} #map specieid -> Specie : for the constant specices that acts like parameters
        self.parameters = {} #map identifier -> Parameter
        self.functions = {}
        
        paramindex, specieindex = 0,0

        for function in sbml_mdl.getListOfFunctionDefinitions():
            self.functions[function.getId()] = Function(function)
        for param in sbml_mdl.getListOfParameters():
            self.parameters[param.getId()] = Parameter(paramindex, param)
            paramindex += 1

        for specie in sbml_mdl.getListOfSpecies():
            if specie.getBoundaryCondition() or specie.getConstant():
                s = Specie(paramindex, specie)
                self.parametersspecies[specie.getId()] = s
                paramindex += 1
            else:
                s = Specie(specieindex, specie)
                self.species[specie.getId()] = s
                specieindex += 1


        for reaction in sbml_mdl.getListOfReactions():
            reactionid=reaction.getId()
            self.reactions[reactionid]=reaction
            for reactant in reaction.getListOfReactants():
                self.addReactionToSpecie(reactant.getSpecies(), reactionid)
            for product in reaction.getListOfProducts():
                self.addReactionToSpecie(product.getSpecies(), reactionid)
            for modifier in reaction.getListOfModifiers():
                self.addReactionToSpecie(modifier.getSpecies(), reactionid)
        print (f"Found {len(self.species)} species, {len(self.reactions)} reactions, {len(self.parameters)} parameters, {len(self.parametersspecies)} species considered as parameters and {len(self.functions)} function definitions.")
    
    def addReactionToSpecie (self, specieid, reactionid):
        try:
            self.species[specieid].addReaction(reactionid)
        except KeyError:
            if self.parametersspecies[specieid] != None:
                self.parametersspecies[specieid].addReaction(reactionid)
            else:
                raise KeyError(f"{specieid} in {reactionid} not registered in the list of species")

        
    def build (self):
        exprs = []
        species_symbol_map = map(lambda specie: (sympy.symbols(specie.internal.getId()), specie.symbol),
                                 self.species.values())
        paramspecies_symbol_map = map(lambda specie: (sympy.symbols(specie.internal.getId()), specie.symbol),
                                      self.parametersspecies.values())
        param_symbol_map = map(lambda param: (sympy.symbols(param.internal.getId()), param.symbol),
                                 self.parameters.values())

        symbol_map = dict(species_symbol_map) | dict(paramspecies_symbol_map) | dict(param_symbol_map)
        function_map = dict(map(lambda function: (function.symbol, function.expr), self.functions.values()))



        for specie in self.species.values():
            expr = specie.buildDifferentialEquation(self.reactions)
            expr=expr.subs(symbol_map)
            for function in self.functions.values():
                expr=function.apply(expr)
            exprs.append(expr)
            print (f"{specie.internal.getId()}|{specie.symbol}: ", expr)





def test():
    system = DiffEqSystem(mdl)
    return system

mdl = libsbml.readSBML("examples/BIOMD0000000056_decomposition_r1.xml").getModel()
mdl = libsbml.readSBML("examples/BIOMD0000000095_decomposition_r1.xml").getModel()
#mdl = libsbml.readSBML("example1.xml").getModel()
