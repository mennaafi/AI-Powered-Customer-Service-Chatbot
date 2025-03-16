import google.generativeai as genai
import os
import json
from copy import deepcopy
from dotenv import load_dotenv 
from .utils import get_chatbot_response

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)


class GuardAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=self.api_key)
        self.model_name = os.getenv("MODEL_NAME", "gemini-1.5-flash")
        
        self.model = genai.GenerativeModel(self.model_name)

    def get_response(self,messages):
        messages = deepcopy(messages)

        system_prompt = """
            You are a helpful AI assistant for a coffee shop application which serves drinks and pastries.
            Your task is to determine whether the user is asking something relevant to the coffee shop or not.
            The user is allowed to:
            1. Ask questions about the coffee shop, like location, working hours, menue items and coffee shop related questions.
            2. Ask questions about menue items, they can ask for ingredients in an item and more details about the item.
            3. Make an order.
            4. ASk about recommendations of what to buy.

            The user is NOT allowed to:
            1. Ask questions about anything else other than our coffee shop.
            2. Ask questions about the staff or how to make a certain menue item.

            Your output should be in a structured json format like so. each key is a string and each value is a string. Make sure to follow the format exactly:
            {
            "chain of thought": go over each of the points above and make see if the message lies under this point or not. Then you write some your thoughts about what point is this input relevant to.
            "decision": "allowed" or "not allowed". Pick one of those. and only write the word.
            "message": leave the message empty if it's allowed, otherwise write "Sorry, I can't help with that. Can I help you with your order?"
            }
            """
        input_messages = [{"role": "model", "parts": system_prompt}] + [messages[-1]]
        chatbot_output = get_chatbot_response(input_messages).text
        output = self.postprocess(chatbot_output)
        
        return output

    def postprocess(self,output):
        cleaned_output = "\n".join(output.splitlines()[1:]).strip('`')
        output = json.loads(cleaned_output)

        dict_output = {
            "role": "assistant",
            "parts": output['message'],
            "memory": {"agent":"guard_agent",
                       "guard_decision": output['decision']
                      }
        }
        return dict_output
    
