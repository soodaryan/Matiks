question_template_prompt = """
    Question: {}

    Solution: {}

    Create templates for these question and solution by adding variables and keeping the language same. Also give me all the variables and mathematical relations between them in json format. Enclose variables in curly brackets in json too.

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

Operators: [+, -, *, /]

Given is the question and the available variables. Convert this question to a single mathematical equation with the given operators. Enclose the variables in curly brackets. Just output the equation in string format.
"""


hints_prompt = """
Question: {}

Solution: {}

Generate 3 hints that incrementally guide towards the solution without revealing it. Each hint must be 10-15 words long. Ensure the hints maintain the same language and context as the question. 

Format: {}

Return only a formatted JSON and do not include any explanations
"""


hints_format = """
[
    "<hint1>", 
    "<hint2>", 
    "<hint3>"
]
"""


category_prompt = """Categorize the given question into the following *superclasses* of mathematics problems, and then into a specific *subclass*:  

*Superclasses*:  
1. **Sequences and Patterns**: Problems focused on identifying, extending, or analyzing numerical or visual patterns and sequences.  
2. **Number Theory**: Problems exploring properties and relationships of numbers, including primes, factors, and numeric puzzles.  
3. **Algebra and Arithmetic Operations**: Problems involving algebraic equations, expressions, and arithmetic operations such as applying BODMAS.  
4. **Real-Life Applications**: Problems with practical scenarios, including work rates, financial transactions, conversions, and dates or calendars.  
5. **Probability and Statistics**: Problems centered on analyzing data, calculating probabilities, or interpreting statistical measures.  
6. **Geometry**: Problems related to shapes, angles, sizes, and spatial reasoning, including area, perimeter, volume, and geometric properties.  

*Subclasses*:  
1. Sequences and Patterns: Arithmetic Sequences, Geometric Sequences, Mixed Sequences, Odd One Out.  
2. Number Theory: Prime Numbers, Factorization Problems, Number Puzzle.  
3. Algebra and Arithmetic Operations: Algebra, BODMAS.  
4. Real-Life Applications: Algebra, Time and Work Problems, Profit and Loss, Currency and Exchange, Calendar Problems.  
5. Probability and Statistics: Probability and Statistics.  
6. Geometry: Area and Perimeter, Volume, Angles, Triangles, Circles, Quadrilaterals, Spatial Reasoning.  

*Question*: {}  

Return the *superclass* and the *subclass* of the math problem without any reasoning or explanations.  

*Format*: {}
"""


category_format = """{
    "superclass": "<superclass of the question>",
    "subclass": "<subclass of the question>"
}"""