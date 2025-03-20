# app/services/embedding_service.py
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.config import settings
import json

class EmbeddingService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
    
    def split_text(self, text):
        """Split a document into chunks."""
        return self.text_splitter.split_text(text)
    
    async def generate_embeddings(self, texts):
        """Generate embeddings for a list of text chunks."""
        embeddings = await self.embeddings.aembed_documents(texts)
        return embeddings
    
    def embeddings_to_json(self, embeddings):
        """Convert embeddings to JSON-serializable format."""
        return json.dumps(embeddings)
    
    def json_to_embeddings(self, json_str):
        """Convert JSON string back to embeddings."""
        return json.loads(json_str)