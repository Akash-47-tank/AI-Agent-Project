"""
Agent Service - Main AI Agent Logic
"""
from typing import Dict, List, Optional
from app.services.llm_service import LLMService
from app.services.rag_service import RAGService
from app.services.memory_service import MemoryService
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class AgentService:
    def __init__(self):
        self.llm_service = LLMService()
        self.rag_service = RAGService()
        self.memory_service = MemoryService()
        
    async def process_query(self, query: str, session_id: Optional[str] = None) -> Dict:
        """
        Main agent logic to process user query
        """
        try:
            # Get conversation history
            history = []
            if session_id:
                history = self.memory_service.get_history(session_id)
            
            # Decide if RAG is needed
            needs_rag = self._needs_document_search(query)
            
            sources = []
            context = ""
            
            if needs_rag:
                logger.info("Query requires document search")
                # Retrieve relevant documents
                docs = await self.rag_service.retrieve_documents(query)
                sources = [doc["source"] for doc in docs]
                context = "\n\n".join([doc["content"] for doc in docs])
            
            # Generate response
            answer = await self.llm_service.generate_response(
                query=query,
                context=context,
                history=history
            )
            
            # Store in memory
            if session_id:
                self.memory_service.add_interaction(
                    session_id=session_id,
                    query=query,
                    answer=answer
                )
            
            return {
                "answer": answer,
                "source": list(set(sources)) if sources else []
            }
            
        except Exception as e:
            logger.error(f"Error in agent processing: {str(e)}")
            raise
    
    def _needs_document_search(self, query: str) -> bool:
        """
        Determine if query needs document search
        """
        keywords = [
            "policy", "document", "guideline", "procedure",
            "according to", "what does", "explain", "describe",
            "faq", "how to", "technical", "specification"
        ]
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in keywords)
    
    def get_session_history(self, session_id: str) -> List[Dict]:
        """Get conversation history"""
        return self.memory_service.get_history(session_id)