import re
import random


def validate_relations(equation, resp):
    var_val = {}
    target_patterns = [
        r"\\boxed\{\{(.*?)\}\}", 
        r"\\boxed\{(.*?)\}",      
        r"oxed\{\{(.*?)\}\}"     
        r"\$\boxed\{\{(.*?)\}\}\$",
        r"\$[\x08]?oxed\{\{(.*?)\}\}\$"
    ]
    
    target = None
    for pattern in target_patterns:
        match = re.search(pattern, resp['solution'])
        if match:
            target = match.group(1)
            break  # Stop once a match is found
    
    if target:
        print(f"Extracted value: {target}")
    else:
        print("No match found for any of the patterns.")

    for i in resp['variable_relations']['variables']:
        if i != target and target is not None:
            var_val[i] = random.randint(1,9)
        elif target is None:
            print("target is none...")
    print("target achieved")
    var_pattern = r"{\b([a-zA-Z_][a-zA-Z0-9_]*)\b}" 
    relations = resp['variable_relations']['relations']
    
    for key, val in relations.items():
        vars = re.findall(var_pattern, val)
    
        for j in vars:
            print(f"Processing variable: {j}")
            print(f"Value: {val}")
            val = val.replace(f"{j}", str(var_val[j])).replace("{", "").replace("}", "")
            print(f"Replacing {j} with value: {var_val[j]}")

        var_val[key] = eval(val)
        print("ook")
        print("var val key: ",var_val[key])
        
    # Replace variable names in the equation
    for key, val in var_val.items():
        if key in equation.lower():
            equation = equation.replace(key, str(val))
            
    
    # Cleanup the equation to make it evaluable
    equation = equation.replace("{", "").replace("}", "")
    equation = equation.replace("=", "==")
    
    print(f"Final equation: {equation}")

    return eval(equation)
