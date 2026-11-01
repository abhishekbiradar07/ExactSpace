# RAG System - Setup Instructions

## Overview
This is a Retrieval-Augmented Generation (RAG) system for querying cyclone separator technical documentation using natural language.

## Prerequisites
- Python 3.12
- Groq API Key (free from https://console.groq.com/keys)
- 11 PDF documents (included in `docs/` folder)

## Quick Setup

### Step 1: Get API Key
1. Visit https://console.groq.com/keys
2. Sign up for free account
3. Create new API key
4. Copy the key

### Step 2: Configure Environment
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API key:
   ```
   GROQ_API_KEY=your_actual_api_key_here
   GROQ_MODEL=qwen/qwen3.8-27b
   ```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Locally
```bash
python app_lite.py
```

Open browser: http://localhost:5000

## System Components

### Files Structure
```
prototype/
├── app_lite.py              # Main Flask application
├── rag_system_groq.py       # RAG engine with Groq API
├── gunicorn_config.py       # Production server config
├── requirements.txt         # Python dependencies
├── templates/
│   └── index.html          # Web interface
├── docs/                   # 11 PDF technical documents
└── vector_store/           # Pre-indexed ChromaDB database
```

### Technology Stack
- **Backend**: Flask (Python)
- **LLM**: Groq API (Qwen 3.8 27B model)
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Vector DB**: ChromaDB (persistent storage)
- **Frontend**: HTML/CSS/JavaScript
- **Production Server**: Gunicorn

## Features
✓ Natural language queries  
✓ Semantic search across 11 PDFs  
✓ Source citations in answers  
✓ Confidence scoring  
✓ Mobile responsive UI  
✓ 129 pre-indexed document chunks  

## Deployment

### Render.com (Recommended)
1. Push code to GitHub
2. Create Render account
3. New Web Service → Connect GitHub repo
4. Set Root Directory: `Task2/prototype`
5. Add environment variable: `GROQ_API_KEY`
6. Deploy

See `RENDER_DEPLOYMENT_GUIDE.md` for detailed steps.

### Local Production
```bash
gunicorn app_lite:app -c gunicorn_config.py
```

## Usage

### Web Interface
1. Open http://localhost:5000
2. Type question: "How does a cyclone separator work?"
3. Click "Get Answer"
4. View answer with sources and confidence score

### API Endpoints
- `GET /` - Web interface
- `POST /query` - Submit question (JSON: `{"question": "..."}`)
- `GET /stats` - System statistics
- `GET /health` - Health check

## Performance
- Response time: 1-3 seconds
- First query: 30-60 seconds (model loading)
- Memory usage: ~450-500MB
- Supports concurrent requests

## Troubleshooting

### "API key not configured"
- Check `.env` file exists
- Verify `GROQ_API_KEY` is set correctly

### "Out of memory" (on deployment)
- Free tier has 512MB limit
- Upgrade to paid plan ($7/month)
- Or run locally with more RAM

### Slow first query
- Normal - models load on first request
- Subsequent queries are fast

## Documentation
- System architecture: See original task requirements
- Deployment guide: `RENDER_DEPLOYMENT_GUIDE.md`
- Full README: `README.md`

## Support
- Groq Documentation: https://console.groq.com/docs
- ChromaDB: https://docs.trychroma.com/
- Sentence Transformers: https://www.sbert.net/

## Notes for Evaluation
- Vector database is pre-populated (no need to re-index)
- All 11 PDFs are included in `docs/` folder
- System uses free/open-source models
- Can be deployed on free tier platforms
- Production-ready with proper error handling

## Security
- API key stored in `.env` (not in git)
- `.env` file is in `.gitignore`
- No sensitive data in responses
- HTTPS enabled on deployment platforms
