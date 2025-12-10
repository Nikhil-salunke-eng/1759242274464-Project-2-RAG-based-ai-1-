# 🎓 RAG AI Teaching Assistant

A Retrieval-Augmented Generation (RAG) based AI teaching assistant that helps students find relevant content in course videos using semantic search and LLM-powered responses.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Local Setup](#local-setup)
- [Running the Application](#running-the-application)
- [Deployment](#deployment)
- [Environment Variables](#environment-variables)
- [Usage Guide](#usage-guide)

## ✨ Features

- 🔍 Semantic search across course video transcripts
- 🤖 Multiple LLM provider support (Ollama, OpenAI, Anthropic)
- 🎯 Precise video section recommendations with timestamps
- 🌐 Web-based interface using Streamlit
- 🐳 Docker support for easy deployment
- ☁️ Ready for cloud deployment (Render, Railway, etc.)

## 🛠 Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.11+
- **ML/AI**: 
  - scikit-learn (cosine similarity)
  - pandas, numpy (data processing)
  - joblib (model serialization)
- **LLM Providers**: 
  - Ollama (local)
  - OpenAI API
  - Anthropic API
- **Deployment**: Docker, Render, Railway

## 📁 Project Structure

```
.
├── app.py                 # Streamlit web application
├── rag_core.py            # Core RAG functionality
├── process_incoming.py    # Original CLI script
├── preprocess_json.py     # JSON preprocessing script
├── mp3_to_json.py        # Audio transcription script
├── video_to_mp3.py       # Video conversion script
├── embeddings.joblib      # Pre-computed embeddings (required)
├── jsons/                # JSON transcript files
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── render.yaml           # Render deployment config
├── railway.json          # Railway deployment config
└── README.md             # This file
```

## 🚀 Local Setup

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- (Optional) Docker and Docker Compose
- (Optional) Ollama installed locally (for local LLM)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <project-directory>
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example config file
   cp config.env.example .env
   
   # Edit .env with your configuration
   # For local Ollama usage, ensure Ollama is running on localhost:11434
   # For cloud LLMs, add your API keys
   ```

5. **Ensure embeddings file exists**
   - The `embeddings.joblib` file must be present in the project root
   - If missing, run the preprocessing pipeline (see [Usage Guide](#usage-guide))

## 🏃 Running the Application

### Option 1: Streamlit (Recommended)

```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

### Option 2: Docker Compose

```bash
docker-compose up --build
```

### Option 3: Docker

```bash
docker build -t rag-assistant .
docker run -p 8501:8501 \
  -e OLLAMA_URL=http://host.docker.internal:11434 \
  -v $(pwd)/embeddings.joblib:/app/embeddings.joblib \
  rag-assistant
```

### Option 4: Original CLI Script

```bash
python process_incoming.py
```

## ☁️ Deployment

### Recommended Platform: **Render** or **Railway**

Both platforms support Python applications and provide easy GitHub integration.

### Deployment Options Comparison

| Platform | Best For | Pros | Cons |
|----------|----------|------|------|
| **Render** | Simple deployments | Free tier, easy setup | Limited resources on free tier |
| **Railway** | Docker deployments | Good Docker support, flexible | Pricing can scale |
| **Streamlit Cloud** | Streamlit apps | Native Streamlit support | Requires Streamlit-specific setup |
| **Vercel** | Not recommended | - | Not ideal for Python ML apps |

### 🚢 Deploy to Render

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Create a Render account**
   - Go to [render.com](https://render.com)
   - Sign up/login with GitHub

3. **Create a new Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect `render.yaml`

4. **Configure Environment Variables**
   - In the Render dashboard, go to Environment
   - Add the following variables:
     ```
     OPENAI_API_KEY=your_key_here
     # OR
     ANTHROPIC_API_KEY=your_key_here
     ```
   - **Important**: For production, use cloud LLM APIs (OpenAI/Anthropic) as Ollama requires local installation

5. **Deploy**
   - Render will automatically build and deploy
   - Your app will be available at `https://your-app-name.onrender.com`

### 🚂 Deploy to Railway

1. **Push your code to GitHub** (same as Render)

2. **Create a Railway account**
   - Go to [railway.app](https://railway.app)
   - Sign up/login with GitHub

3. **Create a new project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

4. **Configure Environment Variables**
   - In Railway dashboard, go to Variables
   - Add:
     ```
     OPENAI_API_KEY=your_key_here
     PORT=8501
     ```

5. **Deploy**
   - Railway will detect `railway.json` and `Dockerfile`
   - Automatic deployment will start
   - Your app will be available at `https://your-app-name.up.railway.app`

### 📝 Important Deployment Notes

1. **LLM Provider Selection**:
   - **Production**: Use OpenAI or Anthropic APIs (recommended)
   - **Local Development**: Ollama works great
   - Ollama requires significant resources and is not suitable for cloud deployment without dedicated infrastructure

2. **File Size Considerations**:
   - `embeddings.joblib` should be committed to the repository
   - Ensure it's not too large (< 100MB recommended)
   - For larger files, consider using cloud storage (S3, etc.)

3. **Environment Variables**:
   - Never commit `.env` file
   - Set all sensitive variables in the deployment platform's dashboard

## 🔧 Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OLLAMA_URL` | Ollama server URL | `http://localhost:11434` | No* |
| `EMBEDDING_MODEL` | Embedding model name | `bge-m3` | No |
| `LLM_MODEL` | LLM model name | `llama3.2` | No |
| `OPENAI_API_KEY` | OpenAI API key | - | No* |
| `ANTHROPIC_API_KEY` | Anthropic API key | - | No* |
| `EMBEDDINGS_PATH` | Path to embeddings file | `embeddings.joblib` | No |
| `PORT` | Server port | `8501` | No |

*At least one LLM provider must be configured

## 📖 Usage Guide

### Preparing Your Data

1. **Collect Videos**
   - Place video files in a `videos/` folder

2. **Convert Videos to MP3**
   ```bash
   python video_to_mp3.py
   ```
   - Creates `audios/` folder with MP3 files

3. **Transcribe MP3 to JSON**
   ```bash
   python mp3_to_json.py
   ```
   - Requires Whisper model (large-v2)
   - Creates JSON files in `jsons/` folder

4. **Generate Embeddings**
   ```bash
   python preprocess_json.py
   ```
   - Requires Ollama running with `bge-m3` model
   - Creates `embeddings.joblib` file

### Using the Web Interface

1. Start the Streamlit app
2. Select your LLM provider in the sidebar
3. Enter your API keys if using cloud providers
4. Type your question in the input field
5. Click "Search" to get answers with relevant video sections

### Example Questions

- "Where is HTML concluded in this course?"
- "What video covers CSS selectors?"
- "Explain the box model"

## 🐛 Troubleshooting

### Common Issues

1. **Embeddings file not found**
   - Ensure `embeddings.joblib` exists in the project root
   - Run the preprocessing pipeline if missing

2. **Ollama connection error**
   - Ensure Ollama is running: `ollama serve`
   - Check `OLLAMA_URL` environment variable
   - For Docker, use `host.docker.internal:11434`

3. **API key errors**
   - Verify API keys are set correctly
   - Check API key permissions and quotas

4. **Port already in use**
   - Change the port: `streamlit run app.py --server.port 8502`
   - Or kill the process using the port

## 📄 License

[Add your license here]

## 🤝 Contributing

[Add contribution guidelines]

## 📧 Support

[Add support contact information]

---

**Made with ❤️ for better learning experiences**
