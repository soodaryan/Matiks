import os
import math
import sys
import json
import vertexai
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv 
from google.cloud import bigquery
from google.oauth2 import service_account
from vertexai.language_models import TextEmbeddingModel


load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
BIG_QUERY_AUTH = os.getenv('BQ_AUTH')

PROJECT_ID = 'matiks-question-generator'
REGION = 'us-central1'

CREDENTIALS = service_account.Credentials.from_service_account_file(BIG_QUERY_AUTH)

BASE_PROMPT = """
    Topic: {topic}
    Question: {question}
    Answer: {answer}

    For the above given question-answer infer subcategories for the topic that are used to solve this question. Identify 7 subcategories and then return them in this format: <topic>: <subcategories>

    Focus on ***jargon and technical terms more to get a better sense of what can be the subcategories.*** Avoid general arithmetic operations like addition and subtraction unless they are specific to the topic. For example, in the case of Profit and Loss, include subcategories like profit percentage, cost price, selling price, and gain/loss. 
    
    **Exclude general operations like addition or subtraction unless directly tied to the topic.**
    
    **Do not output any reasoning just one line.**
    """

SCHEMA = [
    bigquery.SchemaField("question", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("solution", "STRING", mode="REQUIRED"),

    bigquery.SchemaField(
        "variable_relations", "RECORD", mode="NULLABLE", fields=[
            bigquery.SchemaField("variables", "STRING", mode="REPEATED"),

            bigquery.SchemaField("relations", "JSON", mode="NULLABLE"),

            bigquery.SchemaField("constraints", "JSON", mode="NULLABLE")
        ]
    ),

    bigquery.SchemaField("hints", "STRING", mode="REPEATED"),
    bigquery.SchemaField("category", "RECORD", mode="NULLABLE", fields=[
        bigquery.SchemaField("superclass", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("subclass", "STRING", mode="NULLABLE")
    ]),
    bigquery.SchemaField("difficulty", "FLOAT64", mode="REQUIRED"),
    bigquery.SchemaField("embedding", "FLOAT64", mode="REPEATED")
]

DATASET_ID = "dataset_id_for_storing_questions" # For example question_generator
TABLE_ID = "table_id_for_storing_questions" # For example february_questions, june_questione etc.

class Gemini:
    def __init__(self):
        api_key = GEMINI_API_KEY
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        
    def generate_content(self, prompt):
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except ValueError as e:
            raise RuntimeError(f"Authentication failed: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Error generating content: {str(e)}")
        
def init_vertexai_proj():
    vertexai.init(project=PROJECT_ID, location=REGION)
    return

def init_embedding_model():
    embedding_model = TextEmbeddingModel.from_pretrained('textembedding-gecko')
    return embedding_model

def init_bigquery_client():
    client = bigquery.Client(credentials=CREDENTIALS, project=CREDENTIALS.project_id)
    return client

def init_big_query_db(client):
    dataset_ref = client.dataset(DATASET_ID)
    dataset = bigquery.Dataset(dataset_ref)
    client.create_dataset(dataset, exists_ok=True)
    return dataset_ref

def init_big_query_table(client, dataset_ref):
    table_ref = dataset_ref.table(TABLE_ID)
    table = bigquery.Table(table_ref, schema=SCHEMA)
    client.create_table(table, exists_ok=True)
    return table_ref

        
def gen_prompt(base_prompt, question_object):
    prompt = base_prompt.format(topic=question_object["category"], 
                               question=question_object["question"], answer=question_object["solution"])

    return prompt

def get_subclasses_subsubclasses(gemini, prompt):
    try:
        resp = gemini.generate_content(prompt)
        return resp
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def convert_to_embeddings_for_test(embedding_model, subcategory_subsubcategory):
    embedding = np.array(embedding_model.get_embeddings([subcategory_subsubcategory])[0].values)
    return embedding

def numpy_to_python_type(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
        np.int16, np.int32, np.int64, np.uint8,
        np.uint16, np.uint32, np.uint64)):
        return int(obj)
    elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, (np.bool_)):
        return bool(obj)
    elif isinstance(obj, (np.void)): 
        return None
    return obj

def replace_infinity(obj):
    if isinstance(obj, dict):
        return {k: replace_infinity(v) for k, v in obj.items()}
    
    elif isinstance(obj, list):
        return [replace_infinity(item) for item in obj]
    
    elif isinstance(obj, float) and math.isinf(obj):
        return sys.maxsize if obj > 0 else -sys.maxsize
    
    return obj

def fix_relation_constraints(entry):
    if isinstance(entry["variable_relations"]["relations"], dict):
        entry["variable_relations"]["relations"] = json.dumps(entry["variable_relations"]["relations"])
    
    if isinstance(entry["variable_relations"]["constraints"], dict):
        entry["variable_relations"]["constraints"] = json.dumps(entry["variable_relations"]["constraints"])
    
    return entry

def update_big_query_database(json_with_questions):
    init_vertexai_proj()
    client = init_bigquery_client()
    db_ref = init_big_query_db(client)
    table_ref = init_big_query_table(client, db_ref)
    gekko = init_embedding_model()

    gemini = Gemini()

    question_object_to_insert = []
    for question_object in json_with_questions:
        question_object=fix_relation_constraints(replace_infinity(question_object))
        question_object_to_insert.append({
            "question": question_object["question"],
            "solution": question_object["solution"],
            "variable_relations": question_object["variable_relations"],
            "hints": question_object["hints"],
            "category": question_object["category"],
            "difficulty": question_object["difficulty"],
            "embedding": numpy_to_python_type(convert_to_embeddings_for_test(gekko, get_subclasses_subsubclasses(gemini, gen_prompt(BASE_PROMPT, question_object))))
        })

    errors = client.insert_rows_json(table_ref, question_object_to_insert)
    if errors:
        print(f"Errors occured")
        with open("error_log.json", "w+") as f:
            json.dump(errors, f, indent=4)
    else:
        print(f"Added successfully. No errors occured")