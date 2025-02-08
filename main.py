import json
from modules.questions import RandomDataset
from modules.solution import SolutionModel
from modules.llms import OpenAI, Gemini
from modules.validation import validate_relations
from modules.difficulty_model import DifficultyModel
from modules.constraints import Constraints
from modules.vector_db import update_big_query_database
from lib.prompts import question_template_prompt, question_template_format, template_equation_prompt, hints_prompt, hints_format, category_prompt, category_format
from lib.utils import str_to_json, save_json
# from IPython.display import JSON, display
from generate_questions import generate_new_question

def create_template(solution, question):
    gemini = Gemini()

    answer = solution.generate_solution(question) #using deepseek
    print(f"Answer generated: {answer}")
    print()
    question_prompt = question_template_prompt.format(question,  answer, question_template_format)

    response = gemini.generate_content(question_prompt) #using gemini
    
    response = str_to_json(response)
    print("ook")
    response['variable_relations']['relations'] = {k.replace("{", "").replace("}", "") : v for k, v in response['variable_relations']['relations'].items() }
    print()

    question_template = response['question']
    solution_template = response['solution']
    question_variables = response['variable_relations']['variables']

    equation_prompt = template_equation_prompt.format(question_template, question_variables)
    equation = gemini.generate_content(equation_prompt)
    print(equation)
    print()

    is_valid = validate_relations(equation, response)
    
    print(is_valid)
    if is_valid:
        hint_prompt = hints_prompt.format(question_template, solution_template, hints_format)
        hints = gemini.generate_content(hint_prompt)
        print("hints done")
        hints = str_to_json(hints)
        response['hints'] = hints

        categorization_prompt = category_prompt.format(question, category_format)
        category = gemini.generate_content(categorization_prompt)
        print("Categories done")
        category = str_to_json(category)
        response['category'] = category

        difficulty_model = DifficultyModel()
        diff_score = difficulty_model.calculate_score(response, category['subclass'])
        print("Difficulty done")
        response['difficulty'] = diff_score

        constraint_model = Constraints()
        constraints = constraint_model.solve_inequalities(response['variable_relations'])
        print("Constraints done")
        response['variable_relations']['constraints'] = constraints

        return response
    
    else:
        print("Invalid solution generated. Skipping...")

    

if __name__ == "__main__":
    solution = SolutionModel()

    num = int(input('Enter the number of templates to generate: '))

    dataset = RandomDataset("openai/gsm8k")

    data = []
    count = 0

    while count<num:
        questions = dataset.get_random_sample(num-count)
        for ques in questions:
            print(f"Generating template for: {ques}")
            try:
                response = create_template(solution, ques)
                data.append(response)
                print("Template generated successfully!")
                count += 1
                print("="*100)
            except Exception as e:
                print("="*100)
                print(e)
                print()
                print("Some error occurred. Skipping...")
                print("="*100)

    save_path = "question_templates.json"
    save_json(data, save_path)
    manipulated_data = []
    # data = json.dumps(data, indent=4)
    update_big_query_database(data)
    
    for i in data:
        try:
            question_data = generate_new_question(i)
            manipulated_data.append(question_data)
        except Exception as e:
            print("="*60)
            print(e)
            print()
            print("Some error occurred")
            print("="*60)
            continue
    print(data[0])
    update_big_query_database(manipulated_data)
    print("Data saved")