from datasets import load_dataset
import random
import pandas as pd
import math
import re
from lib.utils import find_independent_vars
import sympy as sp
from functools import reduce
import networkx as nx


class RandomDataset:
    def __init__(self, name):
        self.dataset = load_dataset(name, 'main', split='train')
        self.data = pd.DataFrame(self.dataset)

    def get_random_sample(self, num=1):
        n = random.randint(1, len(self.data))
        sample = self.data.sample(num, random_state=n)

        return sample['question'].values.tolist()
    

# class QuestionModel:
#     def __init__(self, max_value=50):
#         self.max_val = max_value
    
#     def _replace_target_var(self, string):
#         target_pattern = r"\\boxed\{\{(.*?)\}\}"
#         target_res = re.search(target_pattern, string)
        
#         span = target_res.span()
#         target = target_res.group(1)
#         res = string[:span[0]] + "{" + f"{target}" + "}" + string[span[1]:]
        
#         return res

#     def _generate_independent_vars(self, variables, constraints, values, index=0):
#         if len(variables) == len(values) or index >= len(variables):
#             return values
        
#         var_name = variables[index]
#         min_val = constraints[var_name][0]
#         max_val = constraints[var_name][1]

#         if max_val == math.inf:
#             max_val = self.max_val
#         else:
#             ind = variables.index(max_val)
#             values = self._generate_independent_vars(variables, constraints, values, ind)
#             max_val = values[max_val]

#         values[var_name] = random.randint(min_val, max_val)

#         return self._generate_independent_vars(variables, constraints, values, index+1)

#     def check_constraints(self, values):
#         is_int = all([isinstance(i, int) for i in values.values()])
#         is_positive = all([i > 0 for i in values.values()])

#         if not is_int or not is_positive:
#             return False
        
#         return True

#     def generate_values(self, variables):
#         var = variables['variables']
#         relations = variables['relations']
#         constraints = variables['constraints']

#         independent_var = find_independent_vars(var, relations)
#         values = self._generate_independent_vars(independent_var, constraints, {})

#         for i in var:
#             if i not in values:
#                 values[i] = eval(relations[i].format(**values))

#         if self.check_constraints(values):
#             return values
        
#         return self.generate_values(variables)

#     def generate_question(self, question):
#         values = self.generate_values(question['variable_relations'])
#         sol = self._replace_target_var(question['solution'])

#         res = {
#             "question": question['question'].format(**values),
#             "solution": sol.format(**values)
#         }

#         return res
    


MAX_VALUE = 20
#get dependent and independent vaiables, make dependency graph, toposort and generate wrt constraints, uses sympy to simplify and test
#returns json, if fails to generate in all constraints, returns none

def compute_variable_relations(data):
    variable_relations = data['variable_relations']
    variables = set(variable_relations["variables"]) 
    constraints = variable_relations["constraints"]
    relations = variable_relations["relations"]
    
    cdep = {var for var, constraint in constraints.items() if isinstance(constraint[1], str) and constraint[1] in variables}
    dependent_vars = set(relations.keys()).union(cdep)
    independent_vars = variables - dependent_vars
    G = nx.DiGraph()
    G.add_nodes_from(variables)
    [G.add_edge(var, dep_var) for dep_var, expr in relations.items() for var in variables if f'{{{var}}}' in expr]
    [G.add_edge(max_val, var) for var, ( _, max_val) in constraints.items() if isinstance(max_val, str) and max_val in variables]
    print(dependent_vars, "\n",independent_vars)
    sympy_vars = {var: sp.Symbol(var) for var in variables}
    sympy_relations = {dep_var : sp.sympify(expr.format(**sympy_vars), locals=sympy_vars) for dep_var, expr in relations.items()}
    solved_expressions = {dep_var : sympy_relations[dep_var] for dep_var in nx.topological_sort(G) if dep_var in sympy_relations}
    failed_states = set()
    independent_value_ranges = {
        var: list(range(max(1, int(constraints[var][0])), int(constraints[var][1]) + 1 if constraints[var][1] != math.inf else MAX_VALUE + 1))
        for var in independent_vars
    }
    print(solved_expressions)
    total_combinations = reduce(lambda a,b:a*b, map(len,independent_value_ranges.values()))
    attempts = 0
    while attempts < total_combinations:
        independent_values = {var: random.choice(independent_value_ranges[var]) for var in independent_vars}
        for temp_dep in cdep: independent_values[temp_dep] = random.randint(constraints[temp_dep][0],independent_values[constraints[temp_dep][1]])
        computed_values , success = independent_values.copy() , True
        for dep_var, expr in solved_expressions.items():
            computed_values[dep_var] = expr.subs(computed_values)
            if not computed_values[dep_var].is_integer or computed_values[dep_var] <= 0:
                failed_states.add(tuple(independent_values.items()))
                success = False
                break
        if success:break
        attempts += 1
    if attempts == total_combinations:return None

    # Extracting only the final values and question template
    result_data = {
        "values": {var: int(computed_values[var]) for var in variables},
        "question": data.get("question", "")
    }

    if not isinstance(result_data, dict):  # Ensure return type is dict
        raise TypeError("Return value must be a dictionary")

    return result_data  # Always returns a dict    
    # if attempts == total_combinations:return None
    # return json.dumps({var:{"relations":str(solved_expressions.get(var,var)),"value": int(computed_values[var])} for var in variables}, indent=4)