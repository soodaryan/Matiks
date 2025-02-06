from modules.llms import OpenAI, Gemini
from modules.difficulty_model import DifficultyModel
from lib.prompts import manipulation_format, manipulation_prompt
from lib.utils import str_to_json, save_json
from modules.questions import compute_variable_relations


def generate_new_question(data):
    result = compute_variable_relations(data)
    difficulty_model = DifficultyModel()
    diff_score = difficulty_model.update_score(result['values'], data['difficulty'])   
    
    result['difficulty'] = data['difficulty']
    result['question'] = result['question'].format(**result['values'])     
    try:
        gemini = Gemini()
        man_prompt = manipulation_prompt.format(result['question'],  manipulation_format)
        res = gemini.generate_content(man_prompt)
        res = str_to_json(res)
        result['manipulated_question'] = res['question'].format(**result['values'])
        result['manipulated_solution'] = res['solution'].format(**result['values'])
    except:
        print('Some error occurred...')

    return result