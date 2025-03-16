from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    MODEL_NAME: str 
    EMBEDDING_MODEL_NAME: str 
    PINECONE_API_KEY: str
    PINECONE_INDEX_NAME: str

    class Config:
        env_file = ".env"

settings = Settings()
