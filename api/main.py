from fastapi import FastAPI
from api.routes import base, chat

app = FastAPI(title="Coffeeshop AI System API")

app.include_router(base.router)  
app.include_router(chat.router)  


