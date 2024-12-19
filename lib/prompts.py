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



category_prompt = """
Question: {}

Categorize the given question into the following types of mathematic problems in accordance with the description: 

Types: 
    Arithmetic Sequences
    Geometric Sequences
    Mixed Sequences
    Prime Numbers
    Factorization Problems
    Odd One Out
    Number Puzzle
    Time and Work Problems
    BODMAS 
    Algebra
    Profit and Loss
    Probability and Statistics
    Currency and Exchange

Description:
    Arithmetic Sequences: Problems involving identifying the next term, common difference, or sum in an arithmetic sequence.  

    Geometric Sequences: Problems related to identifying patterns in multiplicative terms of a sequence.  

    Mixed Sequences: Problems that combine arithmetic and geometric sequences or introduce another type of mathematical series.  

    Prime Numbers: Problems involving recognition of primes, finding missing primes in a range, or identifying composite numbers.  

    Factorization Problems: Problems that identify patterns in divisors, common multiples, or prime factorization.  

    Odd One Out: Problems where you identify odd elements in a list of numbers, shapes, or patterns.  

    Number Puzzle: Problems involving number manipulation, such as reversing digits or finding sums of squares.  

    Time and Work Problems: Problems involving rates, efficiency, or work done by multiple agents working together.  

    BODMAS: Problems based on applying the BODMAS rule to mathematical expressions.  

    Algebra: Problems involving variables and mathematical operations to find unknown values (e.g., solving equations or simplifying expressions).  

    Profit and Loss: Problems involving buying and selling of items, including cost price, selling price, profit/loss calculations, and percentage analysis.  

    Probability and Statistics: Problems based on basic probability, mean, median, mode, or quick statistical interpretations.  

    Currency and Exchange: Problems involving currency conversions, foreign exchange rates, or transactions with multiple constraints.

    Geometry: Problems on shapes, angles, area, perimeter, and volume.  

    Calendar Problems: Questions about days, dates, weeks, intervals, or leap years.

Return only the type of math problem without any reasoning or explanations.
"""