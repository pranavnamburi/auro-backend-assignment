
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.schemas import QuestionRequest, AnswerResponse
from app.services.qa_service import QAService

router = APIRouter(prefix="/qa", tags=["qa"])
qa_service = QAService()

@router.post("/", response_model=dict)
async def answer_question(question_request: QuestionRequest, db: Session = Depends(get_db)):
    response = await qa_service.answer_question(
        db, 
        question_request.question, 
        document_ids=question_request.document_ids
    )
    return response