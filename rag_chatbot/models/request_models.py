from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Source(BaseModel):
    """Model for source information in RAG responses"""
    chapter_id: str
    title: str
    snippet: str
    score: Optional[float] = None

class RAGQueryRequest(BaseModel):
    """Request model for RAG queries"""
    query: str
    selected_text_context: Optional[str] = None

class RAGQueryResponse(BaseModel):
    """Response model for RAG queries"""
    answer: str
    sources: List[Source]
    query_time: datetime = datetime.now()
    mode: str  # "full_book" or "selected_text"