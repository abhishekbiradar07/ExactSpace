# Deployment Guide

## Quick Deploy Options

### Option 1: Render.com (Recommended - Free Tier)

1. Create account at https://render.com
2. Click "New +" -> "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Build Command**: `pip install -r requirements_groq.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Environment Variables**:
     - `GROQ_API_KEY`: your_groq_api_key
     - `GROQ_MODEL`: qwen/qwen3.8-27b
5. Deploy!

### Option 2: Railway.app (Easy Deploy)

1. Create account at https://railway.app
2. Click "New Project" -> "Deploy from GitHub"
3. Select your repository
4. Add environment variables:
   - `GROQ_API_KEY`
   - `GROQ_MODEL`
5. Railway auto-detects Python and deploys

### Option 3: Heroku

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Set env vars:
   ```bash
   heroku config:set GROQ_API_KEY=your_key
   heroku config:set GROQ_MODEL=qwen/qwen3.8-27b
   ```
5. Deploy: `git push heroku main`

### Option 4: Fly.io

1. Install flyctl
2. Run: `fly launch`
3. Set secrets:
   ```bash
   fly secrets set GROQ_API_KEY=your_key
   fly secrets set GROQ_MODEL=qwen/qwen3.8-27b
   ```
4. Deploy: `fly deploy`

### Option 5: Local/VPS Deployment

```bash
# On your server
git clone your-repo
cd Task2/prototype
pip install -r requirements_groq.txt

# Set environment variables
export GROQ_API_KEY=your_key
export GROQ_MODEL=qwen/qwen3.8-27b

# Run with gunicorn
gunicorn app:app --bind 0.0.0.0:8000 --workers 2
```

## Environment Variables Required

- `GROQ_API_KEY` - Get from https://console.groq.com/keys (required)
- `GROQ_MODEL` - Model name (optional, defaults to qwen/qwen3.8-27b)

## Port Configuration

- Development: Port 5000 (default Flask)
- Production: Use `$PORT` environment variable (set by hosting platform)

## Important Notes

1. **Vector Database**: Included in `vector_store/` directory - already populated with 129 chunks
2. **PDF Documents**: In `docs/` folder - already indexed
3. **No Re-indexing Needed**: System ready to use immediately
4. **Free Tier Limits**: Groq free tier = 30 requests/minute

## Monitoring

Check these after deployment:
- Web UI accessible at your deployment URL
- `/stats` endpoint returns system info
- Queries return answers in 2-3 seconds

## Troubleshooting

### Deployment fails
- Check all files uploaded including `vector_store/` folder
- Verify `requirements_groq.txt` installed successfully
- Check environment variables set correctly

### App starts but no answers
- Verify `GROQ_API_KEY` is set
- Check `vector_store/` directory exists
- View logs for error messages

### Timeout errors
- Increase timeout in `Procfile`: `--timeout 120`
- Check Groq API status at console.groq.com

## Cost Estimate

**Free Tier (Development)**:
- Hosting: Free on Render/Railway/Fly.io
- Groq API: Free (30 req/min)
- Total: $0/month

**Production**:
- Hosting: $7-20/month (Railway/Render Pro)
- Groq API: Free tier usually sufficient
- Total: ~$10-20/month

## Security Checklist

- [x] API keys in environment variables (not code)
- [x] `.gitignore` excludes `.env` file
- [x] CORS not enabled (single origin only)
- [x] No sensitive data in responses
- [x] Rate limiting via Groq API (30/min)

## Performance Tips

1. Use Groq's fastest models for production
2. Consider caching frequent queries
3. Monitor response times via logs
4. Set gunicorn workers based on CPU cores

## Backup

Important files to backup:
- `vector_store/` - Your indexed database
- `docs/` - Original PDF documents
- `.env` - Your configuration (keep secure!)
