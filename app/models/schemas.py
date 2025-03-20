
from pydantic import BaseModel, EmailStr
from typing import List, Dict, Optional, Any
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True


class DocumentBase(BaseModel):
    title: str
    content: str
    doc_metadata: Optional[Dict[str, Any]] = None

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class DocumentSelectionRequest(BaseModel):
    document_ids: List[int]


class QuestionRequest(BaseModel):
    question: str
    document_ids: Optional[List[int]] = None  
class AnswerResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]  