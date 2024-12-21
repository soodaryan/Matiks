from modules.questions import RandomDataset
from modules.solution import SolutionModel
from modules.llms import OpenAI
from modules.validation import validate_relations
from modules.difficulty_model import DifficultyModel
from modules.constraints import var_range
from modules.generation import value_replace
from lib.prompts import question_template_prompt, question_template_format, template_equation_prompt, hints_prompt, hints_format, category_prompt
from lib.utils import str_to_json, save_json


def create_template(solution, question):
    openai = OpenAI()

    answer = solution.generate_solution(question)
    print(f"Answer generated: {answer}")
    print()

    question_prompt = question_template_prompt.format(question, answer, question_template_format)

    response = openai.query(question_prompt)
    response = str_to_json(response)

    question_template = response['question']
    solution_template = response['solution']
    question_variables = response['variable_relations']['variables']

    equation_prompt = template_equation_prompt.format(question_template, question_variables)
    equation = openai.query(equation_prompt)

    is_valid = validate_relations(equation, response)

    if is_valid:
        hint_prompt = hints_prompt.format(question_template, solution_template, hints_format)
        hints = openai.query(hint_prompt)
        hints = str_to_json(hints)
        response['hints'] = hints

        categorization_prompt = category_prompt.format(question)
        category = openai.query(categorization_prompt)
        response['category'] = category

        difficulty_model = DifficultyModel()
        diff_score = difficulty_model.calculate_score(response, category)
        response['difficulty'] = diff_score

        return response
    
    else:
        print("Invalid solution generated. Skipping...")


def generate_questions(data):
    ranges = var_range(data)

    ques = [x['question'] for x in data]

    new_ques = value_replace(ranges, ques)

    return new_ques
    

if __name__ == "__main__":
    solution = SolutionModel()

    num = int(input('Enter the number of questions to generate: '))

    dataset = RandomDataset("openai/gsm8k")
    questions = dataset.get_random_sample(num)

    data = []

    for ques in questions:
        print(f"Generating template for: {ques}")
        response = create_template(solution, ques)
        data.append(response)
        print("Template generated successfully!")

    save_path = "question_templates.json"
    save_json(data, save_path)