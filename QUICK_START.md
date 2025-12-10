# ⚡ Quick Start Guide

Get your RAG AI Teaching Assistant up and running in minutes!

## 🚀 Fastest Way to Deploy

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Ready for deployment"
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Step 2: Deploy to Render (5 minutes)

1. Go to [render.com](https://render.com) → Sign up with GitHub
2. Click "New +" → "Web Service"
3. Connect your repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true`
5. Add environment variables:
   - `OPENAI_API_KEY` = your OpenAI key
   - `LLM_MODEL` = `gpt-3.5-turbo`
6. Click "Create Web Service"
7. Wait ~5-10 minutes → Done! 🎉

### Step 3: Deploy to Railway (Alternative)

1. Go to [railway.app](https://railway.app) → Sign up with GitHub
2. "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Add environment variables:
   - `OPENAI_API_KEY` = your OpenAI key
5. Railway auto-deploys → Done! 🎉

## 🏠 Local Development

### Windows
```bash
setup.bat
venv\Scripts\activate
streamlit run app.py
```

### macOS/Linux
```bash
chmod +x setup.sh
./setup.sh
source venv/bin/activate
streamlit run app.py
```

## 🔑 Get API Keys

- **OpenAI**: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Anthropic**: [console.anthropic.com](https://console.anthropic.com)

## ✅ Checklist

- [ ] Code pushed to GitHub
- [ ] `embeddings.joblib` exists in repo
- [ ] API key obtained
- [ ] Environment variables set
- [ ] Deployment started
- [ ] App is live!

## 🆘 Need Help?

- Full guide: [README.md](README.md)
- Deployment details: [DEPLOYMENT.md](DEPLOYMENT.md)
- Issues? Check logs in your platform dashboard

---

**Time to deploy: ~10 minutes** ⏱️

