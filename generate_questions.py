from modules.llms import OpenAI
from modules.difficulty_model import DifficultyModel
from lib.prompts import manipulation_format, manipulation_prompt
from lib.utils import str_to_json, save_json


def generate_new_question(data, question_model):
    values, question = question_model.generate_question(data)

    difficulty_model = DifficultyModel()
    diff_score = difficulty_model.update_score(values, data['difficulty'])        
    question['difficulty'] = diff_score

    try:
        openai = OpenAI()
        man_prompt = manipulation_prompt.format(question, manipulation_format)
        res = openai.query(man_prompt)
        res = str_to_json(res)

        question['manipulated'] = res['question']
    except:
        print('Some error occurred...')

    return question