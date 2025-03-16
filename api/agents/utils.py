import google.generativeai as genai
import os
from dotenv import load_dotenv 
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model_name = os.getenv("MODEL_NAME", "gemini-1.5-flash") 
embedding_model_name = os.getenv("EMBEDDING_MODEL_NAME", "models/text-embedding-004")
model = genai.GenerativeModel(model_name)

def get_chatbot_response(messages):
    input_messages = []
    for message in messages:
        input_messages.append({"role": message["role"], "parts": message["parts"]})

    # Remove 'memory' key
    for msg in messages:
        if "memory" in msg:
            del msg["memory"]

    response = model.generate_content(messages)  
    
    return response


def get_embedding(text_input):
    result = genai.embed_content(
        model=embedding_model_name , 
        content=text_input
    )

    embedding = result['embedding']
    return embedding
