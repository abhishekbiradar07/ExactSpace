# RAG System - Cyclone Separator Documentation

A production-ready Retrieval-Augmented Generation (RAG) system for querying technical documentation about cyclone separators.

## Features

- **Web Interface**: Clean, modern UI for natural language queries
- **Vector Search**: Fast semantic search using ChromaDB with 129 indexed document chunks
- **LLM Generation**: Powered by Groq API (Qwen 3.8 27B model)
- **Source Citations**: All answers cite source documents
- **Confidence Scoring**: Visual indicators for answer reliability
- **11 PDF Documents**: Comprehensive cyclone separator technical manuals

## System Architecture

- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2 (local, 384-dim)
- **Vector Database**: ChromaDB with persistent storage
- **LLM Provider**: Groq API (free tier available)
- **Web Framework**: Flask
- **Frontend**: HTML/CSS/JavaScript (no frameworks)

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements_groq.txt
```

### 2. Set Up Groq API Key

Get a free API key from: https://console.groq.com/keys

Create a `.env` file:

```bash
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=qwen/qwen3.8-27b
```

### 3. Run the Application

```bash
python app.py
```

The server will start at: http://localhost:5000

## Project Structure

```
prototype/
├── app.py                  # Flask web server
├── rag_system_groq.py     # RAG system core logic
├── requirements_groq.txt  # Python dependencies
├── .env                   # Environment variables (API keys)
├── .env.example           # Example environment file
├── .gitignore            # Git ignore rules
├── templates/
│   └── index.html        # Web frontend
├── docs/                 # PDF documentation (11 files)
└── vector_store/         # ChromaDB database
```

## Usage

### Web Interface

1. Open http://localhost:5000
2. Type your question or click example questions
3. View answers with source citations and confidence scores

### Command Line

```bash
# Interactive mode
python rag_system_groq.py --interactive

# Single query
python rag_system_groq.py --query "How does a cyclone separator work?"

# Ingest new documents
python rag_system_groq.py --ingest path/to/pdfs/
```

## Deployment Options

### Local/Development
Already configured - just run `python app.py`

### Production (Heroku, Railway, Render)

1. Add `Procfile`:
```
web: gunicorn app:app
```

2. Install gunicorn:
```bash
pip install gunicorn
```

3. Set environment variables on hosting platform:
   - `GROQ_API_KEY`
   - `GROQ_MODEL`

### Docker

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements_groq.txt .
RUN pip install -r requirements_groq.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## API Endpoints

- `GET /` - Web interface
- `POST /query` - Submit questions (JSON: `{"question": "your query"}`)
- `GET /stats` - System statistics

## Performance

- **Response Time**: 1-3 seconds average
- **Vector Search**: <100ms
- **LLM Generation**: 1-2s
- **Chunks Retrieved**: 5 per query
- **Database Size**: 129 chunks from 11 PDFs

## Configuration

Edit settings in `rag_system_groq.py`:

```python
RAGSystem(
    groq_api_key="...",
    groq_model="qwen/qwen3.8-27b",  # or llama-3.3-70b-versatile
    chunk_size=512,
    chunk_overlap=50,
    top_k=5,
    similarity_threshold=0.1
)
```

## Groq Models Available

- `qwen/qwen3.8-27b` (default, fast and accurate)
- `llama-3.3-70b-versatile` (more powerful)
- `mixtral-8x7b-32768` (longer context)

## Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements_groq.txt
```

### "API key invalid"
- Check `.env` file has correct `GROQ_API_KEY`
- Verify key at https://console.groq.com/keys

### Low confidence scores
- System returns answers with confidence scores
- Low scores indicate partial matches - answers still provided
- Try rephrasing questions to match technical terminology

### Port already in use
```bash
# Change port in app.py:
app.run(port=5001)  # Use different port
```

## License

This is a prototype system for technical documentation queries.

## Support

For issues or questions, check the Groq documentation: https://console.groq.com/docs
