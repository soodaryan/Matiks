import random

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