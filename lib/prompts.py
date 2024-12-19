question_template_prompt = """
    Question: {}

    Solution: {}

    Create templates for these question and solution by adding variables and keeping the language same. Also give me all the variables and relation between them in json format. Enclose variables in curly brackets in json too.

    Format : {}

    Return only a formatted json and don't include any explanations
"""


question_template_format = """
{ 
    question : <question_template>,
    solution : <solution_template>
    variable_relations : {
        "variables": [<variable_names>],
        "relations": {
            "<varaible_name": "{<variable_relation>}"
        }
    }
}
"""


template_equation_prompt = """
Question: {}

Variables: {}

Convert this question to a single algebraic equation. Just output the equation. These are the available variables.
"""