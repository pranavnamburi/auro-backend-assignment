
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.document import Document
from app.models.schemas import DocumentCreate, DocumentResponse, DocumentSelectionRequest
from app.services.document_service import DocumentService
from typing import List

router = APIRouter(prefix="/documents", tags=["documents"])
document_service = DocumentService()

@router.post("/", response_model=DocumentResponse)
async def create_document(
    document: DocumentCreate, 
    background_tasks: BackgroundTasks,
    user_id: int = 1,  # Simplified: we're using a fixed user ID
    db: Session = Depends(get_db)
):
    db_document = Document(
        title=document.title,
        content=document.content,
        user_id=user_id,
        metadata=document.doc_metadata
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    
    
    background_tasks.add_task(document_service.process_document, db, db_document)
    
    return db_document

@router.get("/", response_model=List[DocumentResponse])
def get_documents(
    user_id: int = None, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    documents = document_service.get_documents(db, user_id=user_id, skip=skip, limit=limit)
    return documents

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: int, db: Session = Depends(get_db)):
    document = document_service.get_document(db, document_id=document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@router.delete("/{document_id}", response_model=DocumentResponse)
def delete_document(document_id: int, db: Session = Depends(get_db)):
    document = document_service.delete_document(db, document_id=document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@router.post("/select", response_model=dict)
def select_documents(selection: DocumentSelectionRequest, db: Session = Depends(get_db)):
    
    for doc_id in selection.document_ids:
        if not document_service.get_document(db, doc_id):
            raise HTTPException(status_code=404, detail=f"Document with ID {doc_id} not found")
    
    
    return {"selected_documents": selection.document_ids, "status": "success"}