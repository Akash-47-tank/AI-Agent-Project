"""
Memory Service - Session Management
"""
from typing import List, Dict
from collections import defaultdict
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class MemoryService:
    def __init__(self):
        self.sessions = defaultdict(list)
        self.max_history = 10
    
    def add_interaction(self, session_id: str, query: str, answer: str):
        """Add interaction to session history"""
        try:
            self.sessions[session_id].append({
                "query": query,
                "answer": answer
            })
            
            # Keep only last N interactions
            if len(self.sessions[session_id]) > self.max_history:
                self.sessions[session_id] = self.sessions[session_id][-self.max_history:]
            
            logger.debug(f"Added interaction to session {session_id}")
        except Exception as e:
            logger.error(f"Error adding interaction: {str(e)}")
    
    def get_history(self, session_id: str) -> List[Dict]:
        """Get session history"""
        return self.sessions.get(session_id, [])
    
    def clear_session(self, session_id: str):
        """Clear session history"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Cleared session {session_id}")