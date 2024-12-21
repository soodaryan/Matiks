def value_replace(var_dict, question):
    output_quest = []
    for i, question in enumerate(question):
        key = f'question{i}'  
        try:
            if key in var_dict:
                formatted_question = question.format(**var_dict[key])
                output_quest.append(formatted_question)
        except:
            continue

    return output_quest