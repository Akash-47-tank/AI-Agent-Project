"""
API Routes
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest, QueryResponse
from app.services.agent_service import AgentService
from app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()
agent_service = AgentService()

@router.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    """
    Process user query and return answer
    """
    try:
        logger.info(f"Received query: {request.query[:50]}...")
        
        result = await agent_service.process_query(
            query=request.query,
            session_id=request.session_id
        )
        
        return QueryResponse(**result)
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )

@router.get("/sessions/{session_id}")
async def get_session_history(session_id: str):
    """
    Get conversation history for a session
    """
    try:
        history = agent_service.get_session_history(session_id)
        return {"session_id": session_id, "history": history}
    except Exception as e:
        logger.error(f"Error fetching session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))