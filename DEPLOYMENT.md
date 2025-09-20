# 🚀 Deployment Guide - Homelette Preventivi

## 🐳 Docker Deployment

### Quick Start with Docker Compose

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/homelette-preventivi.git
   cd homelette-preventivi
   ```

2. **Run with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

3. **Access the app:**
   Open your browser to `http://localhost:8501`

### Manual Docker Build

1. **Build the image:**
   ```bash
   docker build -t homelette-preventivi .
   ```

2. **Run the container:**
   ```bash
   docker run -d -p 8501:8501 --name homelette-app homelette-preventivi
   ```

## ☁️ Cloud Deployment Options

### 1. Streamlit Cloud (Recommended)
- Fork this repository on GitHub
- Go to [share.streamlit.io](https://share.streamlit.io)
- Connect your GitHub account
- Deploy from your forked repository
- Set main file to `preventivi_app.py`

### 2. Heroku
1. Install Heroku CLI
2. Create a Heroku app:
   ```bash
   heroku create your-app-name
   ```
3. Add a Procfile:
   ```
   web: streamlit run preventivi_app.py --server.port=$PORT --server.address=0.0.0.0
   ```
4. Deploy:
   ```bash
   git push heroku main
   ```

### 3. DigitalOcean App Platform
1. Connect your GitHub repository
2. Select the repository
3. Set build command: `pip install -r requirements.txt`
4. Set run command: `streamlit run preventivi_app.py --server.headless true --server.port $PORT --server.address 0.0.0.0`

### 4. Google Cloud Run
1. Build and push to Google Container Registry:
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/homelette-preventivi
   ```
2. Deploy to Cloud Run:
   ```bash
   gcloud run deploy --image gcr.io/PROJECT_ID/homelette-preventivi --platform managed --port 8501
   ```

### 5. AWS ECS/Fargate
1. Push image to ECR
2. Create ECS task definition
3. Deploy to Fargate cluster

## 🔧 Environment Variables

For production deployment, you may want to set:

```bash
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

## 📱 Mobile Optimization

The app is already optimized for mobile devices. For best mobile experience:
- Use HTTPS in production
- Enable PWA features if needed
- Consider responsive breakpoints

## 🔒 Security Considerations

For production deployment:
1. Use HTTPS
2. Consider authentication if needed
3. Implement rate limiting
4. Use environment variables for sensitive data
5. Regular security updates

## 📊 Monitoring

- Health check endpoint: `/_stcore/health`
- Metrics available through Streamlit
- Consider adding application monitoring (e.g., Datadog, New Relic)

## 🛠️ Troubleshooting

### Common Issues:
1. **Port conflicts**: Change port in docker-compose.yml
2. **Permission issues**: Check file permissions for logo and documents
3. **Memory issues**: Increase container memory limits
4. **Font issues**: Fonts may not be available in containers (fallbacks are implemented)

### Logs:
```bash
# Docker logs
docker logs homelette-preventivi

# Docker Compose logs
docker-compose logs -f
```
