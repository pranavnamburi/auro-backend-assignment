# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import users, documents, qa
from app.database.db import engine
from app.models import user, document


user.Base.metadata.create_all(bind=engine)
document.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Document Management and RAG-based Q&A API",
    description="API for managing documents and answering questions using RAG",
    
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router)
app.include_router(documents.router)
app.include_router(qa.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Document Management and RAG-based Q&A API"}