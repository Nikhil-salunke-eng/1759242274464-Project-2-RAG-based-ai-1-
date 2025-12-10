# 🚀 Deployment Guide

This guide provides step-by-step instructions for deploying the RAG AI Teaching Assistant to various platforms.

## 📋 Pre-Deployment Checklist

- [ ] Code is pushed to GitHub repository
- [ ] `embeddings.joblib` file exists and is committed
- [ ] Environment variables are documented
- [ ] API keys are ready (OpenAI/Anthropic for production)
- [ ] Dependencies are listed in `requirements.txt`

## 🌐 Platform-Specific Deployment

### Option 1: Render (Recommended for Simplicity)

**Best for**: Quick deployments, free tier available

#### Steps:

1. **Prepare GitHub Repository**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Create Render Account**
   - Visit [render.com](https://render.com)
   - Sign up with GitHub

3. **Create Web Service**
   - Dashboard → "New +" → "Web Service"
   - Connect GitHub repository
   - Select your repository

4. **Configure Service**
   - **Name**: `rag-teaching-assistant` (or your choice)
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Root Directory**: Leave empty (root)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true`

5. **Set Environment Variables**
   - Go to "Environment" tab
   - Add variables:
     ```
     OPENAI_API_KEY=sk-...
     # OR
     ANTHROPIC_API_KEY=sk-ant-...
     EMBEDDING_MODEL=text-embedding-3-small
     LLM_MODEL=gpt-3.5-turbo
     ```

6. **Deploy**
   - Click "Create Web Service"
   - Wait for build to complete (~5-10 minutes)
   - Your app will be live at `https://your-app-name.onrender.com`

#### Render-Specific Notes:
- Free tier spins down after 15 minutes of inactivity
- Upgrade to paid plan for always-on service
- Build time: ~5-10 minutes
- Cold start: ~30-60 seconds

---

### Option 2: Railway (Recommended for Docker)

**Best for**: Docker deployments, flexible configuration

#### Steps:

1. **Prepare GitHub Repository** (same as Render)

2. **Create Railway Account**
   - Visit [railway.app](https://railway.app)
   - Sign up with GitHub

3. **Create New Project**
   - "New Project" → "Deploy from GitHub repo"
   - Select your repository

4. **Configure Deployment**
   - Railway auto-detects `Dockerfile` and `railway.json`
   - No manual configuration needed if files are present

5. **Set Environment Variables**
   - Go to "Variables" tab
   - Add:
     ```
     OPENAI_API_KEY=sk-...
     PORT=8501
     ```

6. **Deploy**
   - Railway automatically builds and deploys
   - View logs in "Deployments" tab
   - Your app will be live at `https://your-app-name.up.railway.app`

#### Railway-Specific Notes:
- Uses Docker for consistent deployments
- Automatic HTTPS
- Pay-as-you-go pricing
- Good for production workloads

---

### Option 3: Streamlit Cloud

**Best for**: Streamlit-native deployments

#### Steps:

1. **Prepare Repository**
   - Ensure `app.py` is in root
   - Create `packages.txt` (if needed):
     ```
     ffmpeg
     ```

2. **Create Streamlit Cloud Account**
   - Visit [streamlit.io/cloud](https://streamlit.io/cloud)
   - Sign up with GitHub

3. **Deploy App**
   - "New app" → Select repository
   - **Main file path**: `app.py`
   - **Python version**: 3.11

4. **Set Secrets**
   - Go to "Settings" → "Secrets"
   - Add:
     ```toml
     [secrets]
     OPENAI_API_KEY = "sk-..."
     ```

5. **Deploy**
   - Click "Deploy"
   - App will be live at `https://your-app-name.streamlit.app`

---

## 🔐 Environment Variables Setup

### For Production (Cloud LLMs)

```bash
# Required
OPENAI_API_KEY=sk-your-key-here
# OR
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Optional
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-3.5-turbo
EMBEDDINGS_PATH=embeddings.joblib
PORT=8501
```

### For Local Development (Ollama)

```bash
OLLAMA_URL=http://localhost:11434
EMBEDDING_MODEL=bge-m3
LLM_MODEL=llama3.2
```

## 🔄 Continuous Deployment

### GitHub Actions (Optional)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Render

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Trigger Render Deploy
        run: |
          curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }}
```

## 📊 Monitoring & Logs

### Render
- View logs: Dashboard → Your Service → "Logs"
- Monitor: Built-in metrics dashboard

### Railway
- View logs: Dashboard → Your Service → "Deployments" → "View Logs"
- Monitor: Railway dashboard metrics

## 🐛 Troubleshooting Deployment

### Build Failures

1. **Check requirements.txt**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify Python version**
   - Ensure Python 3.11+ compatibility

3. **Check file paths**
   - Ensure `embeddings.joblib` exists
   - Verify all imports are correct

### Runtime Errors

1. **Check environment variables**
   - Verify all required variables are set
   - Check API keys are valid

2. **Review logs**
   - Check platform logs for errors
   - Look for import errors or missing files

3. **Test locally first**
   ```bash
   streamlit run app.py
   ```

### Performance Issues

1. **Optimize embeddings file**
   - Compress if too large
   - Consider cloud storage for large files

2. **Upgrade plan**
   - Free tiers have resource limits
   - Consider paid plans for production

## 🔒 Security Best Practices

1. **Never commit API keys**
   - Use environment variables
   - Use platform secrets management

2. **Enable HTTPS**
   - All platforms provide HTTPS by default

3. **Rate limiting**
   - Consider adding rate limits for production
   - Monitor API usage

4. **Input validation**
   - Validate user inputs
   - Sanitize queries

## 📈 Scaling Considerations

- **Traffic**: Start with free tier, upgrade as needed
- **File Size**: Keep `embeddings.joblib` < 100MB
- **API Limits**: Monitor OpenAI/Anthropic usage
- **Caching**: Consider caching frequent queries

## ✅ Post-Deployment Checklist

- [ ] App is accessible via HTTPS
- [ ] Environment variables are set correctly
- [ ] API keys are working
- [ ] Test queries return expected results
- [ ] Logs show no errors
- [ ] Domain is configured (if custom domain)

---

**Need Help?** Check the main [README.md](README.md) or open an issue on GitHub.

