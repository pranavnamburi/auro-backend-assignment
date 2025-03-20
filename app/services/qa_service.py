# app/services/qa_service.py
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from app.config import settings
from app.services.retrieval_service import RetrievalService
from sqlalchemy.orm import Session

class QAService:
    def __init__(self):
        self.retrieval_service = RetrievalService()
        self.llm = ChatOpenAI(
            model_name=settings.LLM_MODEL,
            temperature=0.1,
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        self.qa_prompt = PromptTemplate(
            input_variables=["question", "context"],
            template="""
            You are a helpful assistant that answers questions based on the provided context.
            
            Context:
            {context}
            
            Question: {question}
            
            Answer the question based only on the provided context. If the context doesn't contain the answer, say "I don't have enough information to answer this question."
            
            Answer:
            """
        )
        
        self.qa_chain = LLMChain(llm=self.llm, prompt=self.qa_prompt)
    
    async def answer_question(self, db: Session, question: str, document_ids=None):
        """Answer a question based on retrieved document chunks."""
        # Retrieve relevant chunks
        relevant_chunks = await self.retrieval_service.retrieve_relevant_chunks(
            db, question, document_ids=document_ids
        )
        
        if not relevant_chunks:
            return {
                "answer": "I don't have enough information to answer this question.",
                "sources": []
            }
        
        # Prepare context from chunks
        context = "\n\n".join([chunk[0].content for chunk in relevant_chunks])
        
        # Generate answer
        response = await self.qa_chain.arun(question=question, context=context)
        
        # Prepare sources information
        sources = []
        for chunk, score in relevant_chunks:
            sources.append({
                "document_id": chunk.document_id,
                "chunk_id": chunk.id,
                "relevance_score": float(score),
                "content_preview": chunk.content[:200] + "..." if len(chunk.content) > 200 else chunk.content
            })
        
        return {
            "answer": response,
            "sources": sources
        }