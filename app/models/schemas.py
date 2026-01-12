"""
Pydantic Models
"""
from pydantic import BaseModel, Field
from typing import Optional, List

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="User query")
    session_id: Optional[str] = Field(None, description="Session ID for memory")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is the leave policy?",
                "session_id": "user123"
            }
        }

class QueryResponse(BaseModel):
    answer: str = Field(..., description="AI generated answer")
    source: List[str] = Field(default=[], description="Source documents")
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "According to the policy...",
                "source": ["policy.pdf", "guidelines.txt"]
            }
        }