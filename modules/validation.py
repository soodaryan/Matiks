import re
import random


def validate_relations(equation, resp):
    var_val = {}
    target_pattern = r"\\boxed\{\{(.*?)\}\}"

    target = re.search(target_pattern, resp['solution']).group(1)

    for i in resp['variable_relations']['variables']:
        if i != target:
            var_val[i] = random.randint(1,9)

    var_pattern = r"{(.*?)}"
    relations = resp['variable_relations']['relations']

    for key, val in relations.items():
        vars = re.findall(var_pattern, val)
        for j in vars:
            val = val.replace(f"{j}", str(var_val[j])).replace("{", "").replace("}", "")

        var_val[key] = eval(val)

    for key, val in var_val.items():
        if key in equation.lower():
            equation = equation.replace(key, str(val))

    equation = equation.replace("{", "").replace("}", "")
    equation = equation.replace("=", "==")

    print(equation)

    return eval(equation)