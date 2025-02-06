# PARAMETER EXTRACTION 
import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class OpenAI:
    def __init__(self):
        api_key = os.getenv('ON_DEMAND_API_KEY')

        create_session_url = 'https://api.on-demand.io/chat/v1/sessions'
        self.headers = {
            'apikey': api_key
        }
        session_body = {
            "pluginIds": [],
            "externalUserId": "user"
        }

        response = requests.post(create_session_url, headers=self.headers, json=session_body)
        response_data = response.json()
        self.session_id = response_data['data']['id']


    def query(self, query):
        query_body = {
            "endpointId": "predefined-openai-gpt4o",
            "query": query,
            "pluginIds": [],
            "responseMode": "sync",
            "modelConfigs": { 
                "temperature": 0 
                }
        }

        query_url = f'https://api.on-demand.io/chat/v1/sessions/{self.session_id}/query'

        response = requests.post(query_url, headers=self.headers, json=query_body)
        data = response.json()

        try : 
            return data["data"]["answer"]
        except : 
            return data
        

class Gemini:
    def __init__(self):
        api_key = os.getenv('GENAI_API_KEY')
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash") #gemini-2.0-flash-thinking-exp-01-21
        
    def generate_content(self, prompt):
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except ValueError as e:
            raise RuntimeError(f"Authentication failed: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Error generating content: {str(e)}")