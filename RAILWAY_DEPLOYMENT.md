# Deploy to Railway - Step by Step

Railway.app often handles memory better than Render and has good free tier credits.

## Quick Deploy Steps

### Step 1: Sign Up for Railway

1. Go to: https://railway.app
2. Click "**Login**" (top right)
3. Sign in with GitHub (recommended)
4. Verify your email if needed

### Step 2: Create New Project

1. Click "**New Project**" button
2. Select "**Deploy from GitHub repo**"
3. Click "**Configure GitHub App**"
4. Give Railway permission to access your repositories
5. Select your repository: `EscapeSpace`
6. Click "**Deploy Now**"

### Step 3: Configure Service

Railway will auto-detect it's a Python app. Now configure:

1. Click on your deployment
2. Go to "**Settings**" tab
3. Under "**Root Directory**":
   - Set to: `Task2/prototype`
4. Under "**Build Command**":
   - Should auto-detect: `pip install -r requirements.txt`
5. Under "**Start Command**":
   - Should auto-detect: `gunicorn -c gunicorn_config.py app:app`

### Step 4: Add Environment Variables

1. Click "**Variables**" tab
2. Click "**+ New Variable**"
3. Add:

**Variable 1:**
- Key: `GROQ_API_KEY`
- Value: `[Use your API key from YOUR_CREDENTIALS.txt file]`

**Variable 2:**
- Key: `GROQ_MODEL`
- Value: `qwen/qwen3.8-27b`

**Variable 3:**
- Key: `PYTHON_VERSION`
- Value: `3.12.0`

### Step 5: Deploy

1. Railway will automatically deploy after you add variables
2. Watch the deployment logs (bottom panel)
3. Build takes 3-5 minutes
4. Look for "Success" message

### Step 6: Get Your URL

1. Go to "**Settings**" tab
2. Scroll to "**Domains**" section
3. Click "**Generate Domain**"
4. Your app URL will be something like: `https://escapespace-production.up.railway.app`

### Step 7: Test

1. Click the generated URL
2. Wait 30-60 seconds for first load (model initialization)
3. Try asking: "How does a cyclone separator work?"
4. You should see answer with sources!

## Railway Advantages

✅ Better memory management than Render free tier
✅ $5 free credit per month (enough for development)
✅ Auto-deploys on git push
✅ More generous resource limits
✅ Built-in metrics and logging
✅ Faster cold starts

## Troubleshooting

### Build Fails
- Check Root Directory is `Task2/prototype`
- Verify `requirements.txt` exists
- Check build logs for specific errors

### App Won't Start
- Check environment variables are set
- Verify `GROQ_API_KEY` has no extra spaces
- Look at runtime logs for errors

### Out of Memory
- Railway has better memory handling
- Should work with our optimizations
- Can upgrade plan if needed ($5/month)

### Can't Access URL
- Make sure domain is generated
- Wait 30-60 seconds after first deploy
- Check deployment status is "Active"

## Monitoring

Railway provides:
- **Metrics**: CPU, Memory, Network usage
- **Logs**: Real-time application logs
- **Deployments**: History of all deploys
- **Usage**: Track your free credits

## Cost

**Free Tier:**
- $5 credit per month
- Enough for ~500 hours of usage
- Perfect for development/testing

**Hobby Plan:** $5/month
- More resources
- Priority support
- Better for production

## Auto-Deploy

Every time you push to GitHub, Railway automatically redeploys!

```bash
git add .
git commit -m "Update feature"
git push
```

Railway detects the push and redeploys in 2-3 minutes.

## Your Deployment Info

- **Repository**: https://github.com/abhishekbiradar07/EscapeSpace
- **Root Directory**: Task2/prototype
- **API Key**: [Use YOUR_CREDENTIALS.txt file]
- **Start Command**: gunicorn -c gunicorn_config.py app:app

## Success Checklist

- [ ] Railway account created
- [ ] GitHub connected
- [ ] Repository deployed
- [ ] Root directory set to `Task2/prototype`
- [ ] Environment variables added (GROQ_API_KEY, GROQ_MODEL)
- [ ] Build completed successfully
- [ ] Domain generated
- [ ] Can access the URL
- [ ] Test query returns answer

## Next Steps

1. Generate domain
2. Test your RAG system
3. Share the URL
4. Monitor usage in Railway dashboard

Your Railway app will be live at: `https://[your-service].up.railway.app`

Good luck! 🚂
