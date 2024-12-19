from modules.questions import RandomDataset
from modules.solution import SolutionModel
from modules.llms import OpenAI
from modules.validation import validate_relations
from lib.prompts import question_template_prompt, question_template_format, template_equation_prompt, hints_prompt, hints_format
from lib.utils import str_to_json, save_json


def create_template(question):
    solution = SolutionModel()
    openai = OpenAI()

    answer = solution.generate_solution(question)

    question_prompt = question_template_prompt.format(question, answer, question_template_format)

    response = openai.generate_response(question_prompt)
    response = str_to_json(response)

    question_template = response['question']
    solution_template = response['solution']
    question_variables = response['variable_relations']['variables']

    equation_prompt = template_equation_prompt.format(question_template, question_variables)
    equation = openai.generate_response(equation_prompt)

    is_valid = validate_relations(equation, response)

    if is_valid:
        hint_prompt = hints_prompt.format(question_template, solution_template, hints_format)
        hints = openai.generate_response(hint_prompt)
        response['hints'] = hints

        return response
    
    else:
        return {"error": "Invalid solution generated. Skipping..."}
    

if __name__ == "__main__":
    num = int(input('Enter the number of questions to generate: '))

    dataset = RandomDataset("openai/gsm8k")
    questions = dataset.get_random_sample(num)

    data = []

    for ques in questions:
        response = create_template(ques)
        data.append(response)

    save_path = "question_templates.json"
    save_json(data, save_path)