# AI Agent with RAG - Complete Project

## Architecture Overview

```
┌─────────────┐
│   FastAPI   │
│   Backend   │
└──────┬──────┘
       │
       ├─────► Agent Service (Decision Making)
       │          │
       │          ├─────► LLM Service (OpenAI)
       │          │
       │          ├─────► RAG Service (FAISS + Embeddings)
       │          │
       │          └─────► Memory Service (Session History)
       │
       └─────► API Routes (/ask, /health)
```

## Tech Stack

- **Backend**: FastAPI (Python 3.10+)
- **LLM**: OpenAI GPT-3.5-turbo
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Vector Store**: FAISS
- **Document Processing**: PyPDF2

## Setup Instructions

### Local Setup

1. **Clone and Navigate**
```bash
cd ai-agent-project
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment**
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

5. **Add Documents**
Place your PDF/TXT documents in `data/documents/` directory.

6. **Index Documents**
```bash
python scripts/index_documents.py
```

7. **Run Server**
```bash
python -m app.main
```

Server will start at http://localhost:8000

### API Usage

**Health Check**
```bash
curl http://localhost:8000/health
```

**Ask Question**
```bash
curl -X POST http://localhost:8000/api/v1/ask \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the leave policy?",
    "session_id": "user123"
  }'
```

**Response**
```json
{
  "answer": "According to the company policy...",
  "source": ["sample_policy.txt"]
}
```

## Azure Deployment

### Prerequisites
- Azure account
- Azure CLI installed

### Steps

1. **Create Azure Resources**
```bash
az group create --name ai-agent-rg --location eastus
az appservice plan create --name ai-agent-plan --resource-group ai-agent-rg --sku B1 --is-linux
az webapp create --name ai-agent-app --resource-group ai-agent-rg --plan ai-agent-plan --runtime "PYTHON:3.10"
```

2. **Configure App Settings**
```bash
az webapp config appsettings set --resource-group ai-agent-rg --name ai-agent-app --settings \
  OPENAI_API_KEY="your_key" \
  OPENAI_MODEL="gpt-3.5-turbo"
```

3. **Deploy**
```bash
az webapp up --name ai-agent-app --resource-group ai-agent-rg
```

## Design Decisions

1. **Modular Architecture**: Separated concerns into services for maintainability
2. **FAISS**: Chosen for efficient similarity search without external dependencies
3. **Session-based Memory**: Simple in-memory storage for conversation context
4. **Error Handling**: Comprehensive try-catch blocks with logging
5. **Open Source**: All components are free and open source

## Limitations

1. **Memory**: In-memory session storage (use Redis for production)
2. **Scaling**: Single instance deployment (needs load balancing for scale)
3. **Documents**: Limited to PDF and TXT formats
4. **Authentication**: No built-in auth (add OAuth/JWT for production)

## Future Improvements

1. Add Redis for distributed session management
2. Implement async document processing
3. Add support for more document formats (DOCX, CSV)
4. Implement caching layer for frequent queries
5. Add monitoring and alerting
6. Implement rate limiting
7. Add user authentication
8. Create web UI for easier testing

## Project Structure

```
ai-agent-project/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI entry point
│   ├── api/
│   │   ├── routes.py          # API endpoints
│   ├── services/
│   │   ├── agent_service.py   # Main agent logic
│   │   ├── llm_service.py     # OpenAI integration
│   │   ├── rag_service.py     # Document retrieval
│   │   └── memory_service.py  # Session management
│   ├── models/
│   │   └── schemas.py         # Pydantic models
│   ├── config/
│   │   └── settings.py        # Configuration
│   └── utils/
│       └── logger.py          # Logging setup
├── scripts/
│   └── index_documents.py     # Document indexing
├── data/
│   └── documents/             # Your documents here
├── requirements.txt
├── Dockerfile
└── README.md
```

