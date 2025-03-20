# app/services/document_service.py
from sqlalchemy.orm import Session
from app.models.document import Document, DocumentChunk
from app.models.schemas import DocumentCreate
from app.services.embedding_service import EmbeddingService
import json

class DocumentService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
    
    def create_document(self, db: Session, document: DocumentCreate, user_id: int):
        """Create a new document and generate embeddings for its chunks."""
        # Create the document
        db_document = Document(
            title=document.title,
            content=document.content,
            user_id=user_id,
            metadata=document.metadata
        )
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        
        # Process the document asynchronously
        self.process_document(db, db_document)
        
        return db_document
    
    async def process_document(self, db: Session, document: Document):
        """Process a document by splitting it and generating embeddings."""
        # Split the document into chunks
        chunks = self.embedding_service.split_text(document.content)
        
        # Generate embeddings for each chunk
        embeddings = await self.embedding_service.generate_embeddings(chunks)
        
        # Store chunks and embeddings
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            db_chunk = DocumentChunk(
                document_id=document.id,
                content=chunk,
                embedding=embedding,
                metadata={"chunk_index": i}
            )
            db.add(db_chunk)
        
        db.commit()
    
    def get_document(self, db: Session, document_id: int):
        """Get a document by ID."""
        return db.query(Document).filter(Document.id == document_id).first()
    
    def get_documents(self, db: Session, user_id: int = None, skip: int = 0, limit: int = 100):
        """Get all documents, optionally filtered by user ID."""
        query = db.query(Document)
        if user_id:
            query = query.filter(Document.user_id == user_id)
        return query.offset(skip).limit(limit).all()
    
    def delete_document(self, db: Session, document_id: int):
        """Delete a document by ID."""
        document = db.query(Document).filter(Document.id == document_id).first()
        if document:
            db.delete(document)
            db.commit()
        return document