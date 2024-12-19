import json


def str_to_json(string):
    txt = string.replace("```json", "").replace("```", "")
    return json.loads(txt)