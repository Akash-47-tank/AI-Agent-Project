"""
RAG Service - Document Retrieval
"""
from typing import List, Dict
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import pickle
from pathlib import Path
from app.config.settings import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class RAGService:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.documents = []
        self._load_index()
    
    def _load_index(self):
        """Load FAISS index and documents"""
        try:
            index_path = Path(settings.INDEX_PATH)
            docs_path = Path(settings.DOCUMENTS_PATH)
            
            if index_path.exists() and docs_path.exists():
                self.index = faiss.read_index(str(index_path))
                with open(docs_path, 'rb') as f:
                    self.documents = pickle.load(f)
                logger.info(f"Loaded {len(self.documents)} documents")
            else:
                logger.warning("No index found. Please run indexing first.")
        except Exception as e:
            logger.error(f"Error loading index: {str(e)}")
    
    async def retrieve_documents(
        self,
        query: str,
        top_k: int = 3
    ) -> List[Dict]:
        """
        Retrieve relevant documents for query
        """
        try:
            if self.index is None:
                logger.warning("No index available")
                return []
            
            # Generate query embedding
            query_embedding = self.model.encode([query])
            
            # Search in FAISS
            distances, indices = self.index.search(
                query_embedding.astype('float32'),
                top_k
            )
            
            # Get documents
            results = []
            for idx, dist in zip(indices[0], distances[0]):
                if idx < len(self.documents):
                    doc = self.documents[idx]
                    results.append({
                        "content": doc["content"],
                        "source": doc["source"],
                        "score": float(dist)
                    })
            
            logger.info(f"Retrieved {len(results)} documents")
            return results
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            return []