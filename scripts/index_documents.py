"""
Script to index documents for RAG
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from sentence_transformers import SentenceTransformer
import faiss
import pickle
import PyPDF2
from typing import List, Dict
from app.config.settings import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class DocumentIndexer:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.documents = []
        
    def load_documents(self, docs_dir: str) -> List[Dict]:
        """Load documents from directory"""
        docs_path = Path(docs_dir)
        documents = []
        
        for file_path in docs_path.glob("**/*"):
            if file_path.is_file():
                content = self._read_file(file_path)
                if content:
                    # Split into chunks
                    chunks = self._chunk_text(content, chunk_size=500)
                    for chunk in chunks:
                        documents.append({
                            "content": chunk,
                            "source": file_path.name
                        })
        
        logger.info(f"Loaded {len(documents)} document chunks")
        return documents
    
    def _read_file(self, file_path: Path) -> str:
        """Read file content"""
        try:
            if file_path.suffix == '.pdf':
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text()
                    return text
            elif file_path.suffix in ['.txt', '.md']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception as e:
            logger.error(f"Error reading {file_path}: {str(e)}")
            return ""
    
    def _chunk_text(self, text: str, chunk_size: int = 500) -> List[str]:
        """Split text into chunks"""
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)
        return chunks
    
    def create_index(self, documents: List[Dict]):
        """Create FAISS index"""
        logger.info("Creating embeddings...")
        contents = [doc["content"] for doc in documents]
        embeddings = self.model.encode(contents, show_progress_bar=True)
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings.astype('float32'))
        
        # Save index and documents
        Path("data").mkdir(exist_ok=True)
        faiss.write_index(index, settings.INDEX_PATH)
        with open(settings.DOCUMENTS_PATH, 'wb') as f:
            pickle.dump(documents, f)
        
        logger.info(f"Index created with {len(documents)} documents")

def main():
    indexer = DocumentIndexer()
    documents = indexer.load_documents(settings.DOCUMENTS_DIR)
    if documents:
        indexer.create_index(documents)
    else:
        logger.error("No documents found!")

if __name__ == "__main__":
    main()