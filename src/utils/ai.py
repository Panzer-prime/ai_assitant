import ollama
from ollama import ChatResponse
import json
import os
from pydantic import BaseModel


class output(BaseModel):
    response: str
    functions_called: list[dict[str, str]]


class AI:
    def __init__(self, model, pathToPrompt):

        self.model = model
        self.system_prompt = self.get_system_prompt(pathToPrompt)
        self.model = model


    def get_intent(self, prompt):
        response: ChatResponse = ollama.chat(self.model, messages=[{
            "role": "user",
            "content": self.system_prompt + prompt
        }],
        format="json")

        return json.loads(response.message.content)
    
    
    def get_system_prompt(self, pathToPrompt):
        if not os.path.exists(pathToPrompt):
            print("couldnt get system prompt make sure the file path is right")
            return ""

        with open(pathToPrompt, "r") as file: 
            return file.read()



    def get_ai_response(self, prompt, data = ""):
        
        response: ChatResponse = ollama.chat(self.model, messages=[{
            "role": "user",
            "content": prompt + data
        }],
        format="json")

        return json.loads(response.message.content)




