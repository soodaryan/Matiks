import json


def str_to_json(string):
    txt = string.replace("```json", "").replace("```", "")
    return json.loads(txt)


def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

    return True