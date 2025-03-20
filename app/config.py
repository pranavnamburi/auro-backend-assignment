
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "RAG Document QA"
    
    
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    
    
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    
    LLM_MODEL: str = "gpt-3.5-turbo"  
    
    
    TOP_K_RETRIEVAL: int = 5
    
settings = Settings()