from datasets import load_dataset
import random
import pandas as pd
import math
import re
from lib.utils import find_independent_vars


class RandomDataset:
    def __init__(self, name):
        self.dataset = load_dataset(name, 'main', split='train')
        self.data = pd.DataFrame(self.dataset)

    def get_random_sample(self, num=1):
        n = random.randint(1, len(self.data))
        sample = self.data.sample(num, random_state=n)

        return sample['question'].values.tolist()
    

class QuestionModel:
    def __init__(self, max_value=50):
        self.max_val = max_value
    
    def _replace_target_var(self, string):
        target_pattern = r"\\boxed\{\{(.*?)\}\}"
        target_res = re.search(target_pattern, string)
        
        span = target_res.span()
        target = target_res.group(1)
        res = string[:span[0]] + "{" + f"{target}" + "}" + string[span[1]:]
        
        return res

    def _generate_independent_vars(self, variables, constraints, values, index=0):
        if len(variables) == len(values) or index >= len(variables):
            return values
        
        var_name = variables[index]
        min_val = constraints[var_name][0]
        max_val = constraints[var_name][1]

        if max_val == math.inf:
            max_val = self.max_val
        else:
            ind = variables.index(max_val)
            values = self._generate_independent_vars(variables, constraints, values, ind)
            max_val = values[max_val]

        values[var_name] = random.randint(min_val, max_val)

        return self._generate_independent_vars(variables, constraints, values, index+1)

    def check_constraints(self, values):
        is_int = all([isinstance(i, int) for i in values.values()])
        is_positive = all([i > 0 for i in values.values()])

        if not is_int or not is_positive:
            return False
        
        return True

    def generate_values(self, variables):
        var = variables['variables']
        relations = variables['relations']
        constraints = variables['constraints']

        independent_var = find_independent_vars(var, relations)
        values = self._generate_independent_vars(independent_var, constraints, {})

        for i in var:
            if i not in values:
                values[i] = eval(relations[i].format(**values))

        if self.check_constraints(values):
            return values
        
        return self.generate_values(variables)

    def generate_question(self, question):
        values = self.generate_values(question['variable_relations'])
        sol = self._replace_target_var(question['solution'])

        res = {
            "question": question['question'].format(**values),
            "solution": sol.format(**values)
        }

        return res