# Deploy to Render - Step by Step Guide

## Prerequisites
- GitHub account
- Groq API key from https://console.groq.com/keys
- This code pushed to a GitHub repository

## Step-by-Step Deployment

### Step 1: Push Code to GitHub

If you haven't already:

```bash
cd Task2/prototype

# Initialize git (if needed)
git init

# Add all files
git add .

# Commit
git commit -m "RAG system ready for deployment"

# Create GitHub repo and push
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

**IMPORTANT**: Make sure `.env` is in `.gitignore` (it already is) - DON'T push your API key!

### Step 2: Create Render Account

1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub (recommended) or email
4. Verify your email

### Step 3: Create New Web Service

1. Click "New +" button (top right)
2. Select "Web Service"
3. Choose "Build and deploy from a Git repository"
4. Click "Next"

### Step 4: Connect GitHub Repository

1. Click "Connect Account" under GitHub
2. Authorize Render to access your repositories
3. Find and select your RAG system repository
4. Click "Connect"

### Step 5: Configure Web Service

Fill in these settings:

**Basic Settings:**
- **Name**: `rag-cyclone-separator` (or any name you want)
- **Region**: Choose closest to you
- **Branch**: `main`
- **Root Directory**: `Task2/prototype` ⚠️ IMPORTANT!
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements_groq.txt`
- **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 1`

**Instance Type:**
- Select "Free" (0.1 CPU, 512 MB RAM)

### Step 6: Set Environment Variables

Scroll down to "Environment Variables" section:

Click "Add Environment Variable" and add:

1. **Key**: `GROQ_API_KEY`  
   **Value**: `your_groq_api_key_here`

2. **Key**: `GROQ_MODEL`  
   **Value**: `qwen/qwen3.8-27b`

3. **Key**: `PYTHON_VERSION`  
   **Value**: `3.12.0`

### Step 7: Deploy!

1. Click "Create Web Service" button at the bottom
2. Render will start building your app
3. Watch the deployment logs (this takes 3-5 minutes)

You'll see:
- Installing dependencies
- Downloading embedding model
- Starting server
- "Your service is live" message

### Step 8: Test Your Deployment

1. Once deployed, click the URL at the top (e.g., `https://rag-cyclone-separator.onrender.com`)
2. Your RAG system web interface should load
3. Try asking a question!

## Deployment Timeline

- Initial build: 3-5 minutes
- Subsequent deploys: 2-3 minutes
- Cold start (after inactivity): 30-60 seconds

## Important Notes

### Free Tier Limitations
- App spins down after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds
- 750 hours/month free (enough for development)
- Shared CPU and 512 MB RAM

### First Request After Deploy
The first query may take 30-60 seconds because:
1. Embedding model needs to load (90 MB)
2. Vector database needs to initialize
3. Connection to Groq needs to establish

Subsequent requests: 1-3 seconds

### Auto-Deploy
Every time you push to GitHub, Render will automatically redeploy!

## Troubleshooting

### Build Fails

**Issue**: "No module named 'sentence_transformers'"
- **Fix**: Ensure `requirements_groq.txt` is in `Task2/prototype/` folder
- Check "Root Directory" is set to `Task2/prototype`

**Issue**: "Port 5000 already in use"
- **Fix**: This shouldn't happen on Render (they manage ports)
- Verify start command uses `$PORT` variable

### Runtime Errors

**Issue**: "API key invalid"
- **Fix**: Check environment variable `GROQ_API_KEY` is set correctly
- No spaces or quotes needed

**Issue**: "Collection not found"
- **Fix**: Ensure `vector_store/` folder is in your repo
- Check it wasn't gitignored

**Issue**: Timeout errors
- **Fix**: Already set to 120 seconds in start command
- Free tier has resource limits, this is normal occasionally

### App Won't Load

**Issue**: Gets stuck on loading
- **Fix**: Check Render logs (click "Logs" tab)
- Look for error messages in red
- Verify all environment variables are set

### Low Confidence Answers

**Issue**: All answers show low confidence
- **Fix**: This is working as designed
- System is conservative with confidence scores
- Answers are still generated with available context

## Monitoring

### Check Logs
1. Go to Render dashboard
2. Click your service
3. Click "Logs" tab
4. See real-time logs

### Check Status
- Dashboard shows: Running, Sleeping, or Failed
- Green = Running
- Gray = Sleeping (will wake on request)
- Red = Failed (check logs)

### Metrics (Free Tier)
- Request count
- Response times
- Memory usage
- CPU usage

## Updating Your App

1. Make changes locally
2. Commit: `git commit -am "Update feature"`
3. Push: `git push`
4. Render auto-deploys (2-3 minutes)

## Custom Domain (Optional)

1. Go to your service settings
2. Click "Custom Domain"
3. Add your domain
4. Update DNS records as instructed

## Cost

**Free Tier**: $0/month
- 750 hours/month
- Spins down after inactivity
- Perfect for development/testing

**Starter Plan**: $7/month
- Always on (no spin down)
- 0.5 CPU, 512 MB RAM
- Faster performance

## Security Checklist

✅ API key in environment variables (not code)  
✅ `.env` file in `.gitignore`  
✅ HTTPS enabled automatically by Render  
✅ No sensitive data in logs  
✅ Rate limiting via Groq (30 req/min)  

## Performance Tips

1. **Reduce cold starts**: Upgrade to Starter plan ($7/mo)
2. **Faster model**: Switch to `llama-3.3-70b-versatile`
3. **More workers**: Change `--workers 1` to `--workers 2` (need Starter plan)
4. **Enable caching**: Add Redis for frequent queries (optional)

## Support

- Render Docs: https://render.com/docs
- Render Status: https://status.render.com
- Community: https://community.render.com

## Your Deployment Info

**Repository**: Your GitHub repo  
**Branch**: main  
**Root Directory**: Task2/prototype  
**API Key**: Already configured in .env  
**Model**: qwen/qwen3.8-27b  

## Success Checklist

- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Web service created
- [ ] Root directory set to `Task2/prototype`
- [ ] Environment variables added
- [ ] Build completed successfully
- [ ] URL is live and accessible
- [ ] Test query returns answer
- [ ] Sources and confidence showing

## Next Steps After Deployment

1. Share your URL with stakeholders
2. Monitor usage in Render dashboard
3. Upgrade to Starter if you need always-on
4. Add custom domain if needed
5. Set up monitoring/alerts

**Your app will be live at**: `https://[your-service-name].onrender.com`

Good luck! 🚀
