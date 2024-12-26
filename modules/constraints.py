import random
import sympy as sp
from sympy import *
import math
import re
from lib.utils import find_independent_vars

def check_all_constraints(variables, constraints):
    for var_name, condition in constraints.items():
        condition_check = condition
        for key, value in variables.items():
            condition_check = condition_check.replace(key, str(value))
        try:
            if not eval(condition_check):
                return False
        except Exception as e:
            return False
    return True

def check_negative(num):
        if num<1:
            return False
        else:
            return True

def check_integer(num):
    return isinstance(num, int)

#resp is a list containing the gpt 4 responses which containthe question, solution, relations , variables and constraints of each question
def var_range(resp):
    var_range = {}
    for i in range(len(resp)):
        independent_var = []
        var = resp[i]['variable_relations']['variables']
        dependent_var = resp[i]['variable_relations']['relations'].keys()
        relations = resp[i]['variable_relations']['relations']
        constraints = resp[i]['variable_relations']['constraints']
        for j in var :
            if j not in dependent_var :
                independent_var.append(j)
        
        iteration = 0
        while iteration < 100 :
            try:
                var_range[f'question{i}'] = {}
                for var_name in independent_var:
                    var_range[f'question{i}'][var_name] = random.randint(5, 15)
                for var_name in dependent_var:
                    relation = relations[var_name]
                    k = eval(relation.format(**var_range[f'question{i}']))
                    if not check_integer(k) or not check_negative(k):
                        break
                    var_range[f'question{i}'][var_name] = k
                    
                if check_all_constraints(var_range[f'question{i}'], constraints):
                    break
        
                iteration += 1
            except:
                iteration += 1
    return var_range





class Constraints:
    def count_braces(self, value):
        return value.count('{')

    def sort_dict_by_brace_count(self, d):
        return sorted(d.items(), key=lambda item: self.count_braces(item[1]))

    def extract_range(self, string):
        pattern = r"([a-zA-Z0-9_]+)\s*(<|>|<=|>=)\s*([a-zA-Z0-9_]+|\d+)"
    
        match = re.findall(pattern, string)
    
        lower_bound = 1
        upper_bound = math.inf
        var = ""
    
        for rel in match:
            if rel[1] in [">", ">="]:
                var = rel[-1]
                upper_bound = rel[0]
            elif rel[1] in ["<", "<="]:
                val = rel[0]
                upper_bound = rel[-1]
    
        return lower_bound, upper_bound, var.strip()

    def solve_inequalities(self, data):
        variables = data['variables']
        relations = data['relations']
    
        independent_vars = find_independent_vars(variables, relations)
    
        var_pattern = r"{(.*?)}"
        symbols_dict = {var: Symbol(var) for var in variables}
    
        relations = self.sort_dict_by_brace_count(relations)
        dependent_ranges = {v: (0, math.inf) for v in variables if v not in independent_vars}
        independent_ranges = {}
    
        for var, rel in relations:
            v = re.findall(var_pattern, rel)
    
            rel = rel.format(**symbols_dict)
            rel = rel.replace("{", "").replace("}", "")
    
            for i in v:
                if i in dependent_ranges:
                    rel = rel.replace(f"{i}", str(dependent_ranges[i][0]))
    
            final = sympify(f"{rel} > 0")
    
            if isinstance(final, sp.logic.boolalg.BooleanFalse):
                continue
    
            sol = reduce_inequalities(final, [symbols_dict[v[0]]])
            if sol == final:
                continue
            
            ran = self.extract_range(str(sol))
            if ran[-1] == "":
                continue
            independent_ranges[ran[-1]] = ran[:-1]
    
        for i in independent_vars:
            if i not in independent_ranges:
                independent_ranges[i] = (1, math.inf)
    
        return independent_ranges