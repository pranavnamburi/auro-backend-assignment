# app/services/retrieval_service.py
import numpy as np
from sqlalchemy.orm import Session
from app.models.document import DocumentChunk
from app.services.embedding_service import EmbeddingService
from app.config import settings

class RetrievalService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
    
    async def retrieve_relevant_chunks(self, db: Session, query: str, document_ids=None, top_k=None):
        """Retrieve most relevant document chunks for a query."""
        if top_k is None:
            top_k = settings.TOP_K_RETRIEVAL
        
        # Generate embedding for the query
        query_embedding = await self.embedding_service.generate_embeddings([query])
        query_embedding = query_embedding[0]
        
        # Query the database for all chunks
        query = db.query(DocumentChunk)
        
        # Filter by document IDs if provided
        if document_ids:
            query = query.filter(DocumentChunk.document_id.in_(document_ids))
        
        chunks = query.all()
        
        # Calculate similarity scores
        similarities = []
        for chunk in chunks:
            chunk_embedding = chunk.embedding
            similarity = self._cosine_similarity(query_embedding, chunk_embedding)
            similarities.append((chunk, similarity))
        
        # Sort by similarity (descending) and take top-k
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_chunks = similarities[:top_k]
        
        return top_chunks
    
    def _cosine_similarity(self, embedding1, embedding2):
        """Calculate cosine similarity between two embeddings."""
        dot_product = np.dot(embedding1, embedding2)
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        return dot_product / (norm1 * norm2)