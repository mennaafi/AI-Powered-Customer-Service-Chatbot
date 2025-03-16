import google.generativeai as genai
import os
import json
from copy import deepcopy
from dotenv import load_dotenv 
from .utils import get_chatbot_response , get_embedding
from pinecone import Pinecone
load_dotenv()


class DetailsAgent():
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=self.api_key)
        self.model_name = os.getenv("MODEL_NAME", "gemini-1.5-flash")
        self.model = genai.GenerativeModel(self.model_name)
        self.embedding_model_name = os.getenv("EMBEDDING_MODEL_NAME", "models/text-embedding-004")
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index_name = os.getenv("PINECONE_INDEX_NAME")

    def get_closest_results(self,index_name,input_embeddings,top_k=2):
        index = self.pc.Index(index_name)
        
        results = index.query(
            namespace="ns1",
            vector=input_embeddings,
            top_k=top_k,
            include_values=False,
            include_metadata=True
        )

        return results
    
    def get_response(self,messages):
        messages = deepcopy(messages)
        user_message = messages[-1]['parts']
        embeddings = get_embedding(user_message)
        results = self.get_closest_results(self.index_name,embeddings,top_k=2)
        source_knowledge = "\n".join([x['metadata']['text'].strip()+'\n' for x in results['matches'] ])

        prompt = f"""
        Using the contexts below, answer the query.

        Contexts:
        {source_knowledge}

        Query: {user_message}
        """

        system_prompt = """ You are a customer support agent for a coffee shop called Merry's way. You should answer every question as if you are waiter and provide the neccessary information to the user regarding their orders """
        messages[-1]['parts'] = prompt
        input_messages = [{"role": "model", "parts": system_prompt}] + messages[-3:]
        chatbot_output = get_chatbot_response(input_messages).text
        output = self.postprocess(chatbot_output)
        return output
    

    def  postprocess(self, output):
        output = {
            "role": "assistant",
            "parts": output,
            "memory": {"agent":"details_agent"
                      }
        }
        return output







