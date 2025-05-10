# PODRelay API – Render Deployment

This repository contains the full setup to deploy the `relay_api.py` FastAPI server to [Render](https://render.com), which serves as the structured MTSL message endpoint for GPT agents.

---

## 🚀 Quick Deployment Steps

1. **Push this repo to GitHub**

   You can upload manually or use the command line:

   ```bash
   git init
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git add .
   git commit -m "Initial commit for PODRelay API"
   git push -u origin main
   ```

2. **Create a Web Service on Render**

   - Go to: https://dashboard.render.com/
   - Click **"New Web Service"**
   - Select **"Deploy from GitHub"**
   - Connect your repo
   - Use the following settings:
     - **Environment**: Python
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn relay_api:app --host 0.0.0.0 --port 8000`
     - **Environment Variable**: `PYTHON_VERSION=3.11`
     - **Plan**: Free (if eligible)

3. **Access Your Endpoint**

   After deployment, your FastAPI server will be accessible at:

   ```
   https://your-subdomain.onrender.com/relay
   ```

   You can send MTSL messages via `POST /relay`.

---

## 🛠 Files Included

- `relay_api.py`: Your FastAPI handler
- `concord_session_engine.py`: Orchestration engine for message routing
- `Dockerfile`: Container build script
- `requirements.txt`: Python dependencies
- `render.yaml`: Optional config for Render Blueprint deployment

---

## ✅ Ready to Go

This repo is plug-and-play for Render deployment. Fast, HTTPS-enabled, and GPT-ready.

