from modules.solution import SolutionModel
from modules.llms import OpenAI
from modules.validation import validate_relations
from lib.prompts import question_template_prompt, question_template_format, template_equation_prompt
from lib.utils import str_to_json


def create_template(question):
    solution = SolutionModel()
    openai = OpenAI()

    answer = solution.generate_solution(question)

    question_prompt = question_template_prompt.format(question, answer, question_template_format)

    response = openai.generate_response(question_prompt)
    response = str_to_json(response)

    question_template = response['question']
    question_variables = response['variable_relations']['variables']
    equation_prompt = template_equation_prompt.format(question_template, question_variables)

    equation = openai.generate_response(equation_prompt)

    is_valid = validate_relations(equation, response)

    if is_valid:
        return response
    
    else:
        return {"error": "Invalid solution generated. Skipping..."}
    


if __name__ == "__main__":
    question = input("Enter the question: ")

    print(create_template(question))