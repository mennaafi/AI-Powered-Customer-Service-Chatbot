import google.generativeai as genai
import os
from dotenv import load_dotenv
from copy import deepcopy
import json 
from .utils import get_chatbot_response
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)


class ClassificationAgent():
    def __init__(self):
        self.api_key = api_key  
        self.model_name = os.getenv("MODEL_NAME", "gemini-1.5-flash") 
        self.model = genai.GenerativeModel(self.model_name)
    
    def get_response(self,messages):
        messages = deepcopy(messages)
        system_prompt =  """
            You are a helpful AI assistant for a coffee shop application.
            Your task is to determine what agent should handle the user input. You have 3 agents to choose from:
            1. details_agent: This agent is responsible for answering questions about the coffee shop, like location, delivery places, working hours, details about menue items. Or listing items in the menu items. Or by asking what we have.
            2. order_taking_agent: This agent is responsible for taking orders from the user. It's responsible to have a conversation with the user about the order untill it's complete.
            3. recommendation_agent: This agent is responsible for giving recommendations to the user about what to buy. If the user asks for a recommendation, this agent should be used.

            Your output should be in a structured json format like so. each key is a string and each value is a string. Make sure to follow the format exactly:
            {
            "chain of thought": go over each of the agents above and write some your thoughts about what agent is this input relevant to.
            "decision": "details_agent" or "order_taking_agent" or "recommendation_agent". Pick one of those. and only write the word.
            "message": leave the message empty.
            }
            """
        
            # Remove 'memory' key from all messages before sending
               # Remove 'memory' key from all messages before sending    # Remove 'memory' key from all messages before sending
        for msg in messages:
            if "memory" in msg:
                del msg['memory']



        input_messages = [{"role": "model", "parts": system_prompt}] + [messages[-1]]
        chatbot_output =  get_chatbot_response(input_messages).text

        output = self.postprocess(chatbot_output)
        return output
    
    def postprocess(self,output):
        cleaned_output = "\n".join(output.splitlines()[1:]).strip('`')
        output = json.loads(cleaned_output)

        dict_output = {
            "role": "assistant",
            "parts": output['message'],
            "memory": {"agent":"classification_agent",
                       "classification_decision": output['decision']
                      }
        }
        return dict_output

