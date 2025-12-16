# 🚀 PitchOS Deployment Guide

## 📋 **Complete Production Deployment Setup**

This guide covers deploying both the React frontend and FastAPI backend for PitchOS in production environments.

---

## 🏗️ **Deployment Options**

### **Option 1: Docker Compose (Recommended)**
- ✅ **Easy Setup** - Single command deployment
- ✅ **Scalable** - Container orchestration
- ✅ **Portable** - Works on any Docker host
- ✅ **Production Ready** - Nginx reverse proxy included

### **Option 2: Cloud Platforms**
- **Frontend**: Vercel, Netlify, AWS S3 + CloudFront
- **Backend**: Railway, Heroku, AWS Lambda, Google Cloud Run

### **Option 3: Traditional VPS**
- **Frontend**: Nginx static files
- **Backend**: PM2 process manager

---

## 🐳 **Docker Deployment (Recommended)**

### **Prerequisites**
```bash
# Install Docker and Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### **Quick Start**
```bash
# 1. Clone and setup
git clone <your-repo>
cd PitchOS

# 2. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 3. Deploy with one command
chmod +x deploy.sh
./deploy.sh production
```

### **Manual Docker Deployment**
```bash
# Build images
docker build -f Dockerfile.backend -t pitchos-backend .
docker build -f Dockerfile.frontend -t pitchos-frontend .

# Run with Docker Compose
docker-compose --profile production up -d

# Check status
docker-compose ps
```

---

## ☁️ **Cloud Platform Deployment**

### **Frontend - Vercel**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy frontend
cd frontend
vercel --prod

# Set environment variables in Vercel dashboard:
# VITE_API_URL=https://your-backend-url.com
```

### **Frontend - Netlify**
```bash
# Build locally
cd frontend
npm run build

# Deploy to Netlify
# 1. Drag & drop 'dist' folder to netlify.com
# 2. Or connect GitHub repo for auto-deploy
```

### **Backend - Railway**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy backend
cd backend
railway login
railway init
railway up

# Set environment variables in Railway dashboard
```

### **Backend - Heroku**
```bash
# Install Heroku CLI
# Create Procfile in backend/
echo "web: python -m uvicorn main:app --host 0.0.0.0 --port \$PORT" > backend/Procfile

# Deploy
cd backend
heroku create your-app-name
git push heroku main
```

---

## 🔧 **Environment Configuration**

### **Backend Environment Variables**
```env
# Required
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_CLOUD_VISION_API_KEY=your_vision_key_here

# Optional
DEBUG=False
LOG_LEVEL=INFO
OCR_LANGUAGES=en
OCR_MIN_TEXT_LENGTH=20
IMAGE_MAX_WIDTH=1920
IMAGE_MAX_HEIGHT=1080
```

### **Frontend Environment Variables**
```env
# Production
VITE_API_URL=https://your-backend-domain.com
VITE_APP_NAME=PitchOS
VITE_APP_VERSION=1.0.0
VITE_ENVIRONMENT=production

# Features
VITE_ENABLE_OCR=true
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_DEBUG=false

# Analytics (optional)
VITE_GA_TRACKING_ID=G-XXXXXXXXXX
VITE_HOTJAR_ID=1234567
```

---

## 🌐 **Domain & SSL Setup**

### **Custom Domain**
```bash
# Update nginx.conf
server_name your-domain.com www.your-domain.com;

# DNS Records
A     your-domain.com     -> your-server-ip
CNAME www.your-domain.com -> your-domain.com
```

### **SSL Certificate (Let's Encrypt)**
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

---

## 📊 **Monitoring & Logging**

### **Health Checks**
```bash
# Backend health
curl https://your-domain.com/api/health

# Frontend health
curl https://your-domain.com/

# Docker health
docker-compose ps
```

### **Logs**
```bash
# View all logs
docker-compose logs -f

# Specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Nginx logs
docker-compose logs -f nginx
```

### **Monitoring Setup**
```bash
# Add to docker-compose.yml
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
  
  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
```

---

## 🔄 **CI/CD Pipeline**

### **GitHub Actions**
```yaml
# .github/workflows/deploy.yml
name: Deploy PitchOS
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to production
        run: |
          ssh user@server 'cd /app && git pull && ./deploy.sh production'
```

### **Automated Deployment**
```bash
# Setup webhook for auto-deploy
# 1. Create webhook endpoint
# 2. Configure GitHub webhook
# 3. Auto-deploy on push to main
```

---

## 🛡️ **Security Checklist**

### **Backend Security**
- ✅ **API Keys** - Store in environment variables
- ✅ **CORS** - Configure allowed origins
- ✅ **Rate Limiting** - Prevent abuse
- ✅ **Input Validation** - Sanitize all inputs
- ✅ **HTTPS** - SSL/TLS encryption

### **Frontend Security**
- ✅ **CSP Headers** - Content Security Policy
- ✅ **XSS Protection** - Cross-site scripting prevention
- ✅ **HTTPS** - Secure connections only
- ✅ **Environment Variables** - No secrets in frontend

### **Infrastructure Security**
- ✅ **Firewall** - Block unnecessary ports
- ✅ **Updates** - Keep system updated
- ✅ **Backups** - Regular data backups
- ✅ **Monitoring** - Log analysis and alerts

---

## 🚀 **Performance Optimization**

### **Frontend Optimization**
```bash
# Build optimization
npm run build -- --mode production

# Bundle analysis
npm install -g webpack-bundle-analyzer
npx webpack-bundle-analyzer dist/assets/*.js
```

### **Backend Optimization**
```python
# Add to main.py
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Database connection pooling
# Caching with Redis
# Background tasks with Celery
```

### **Infrastructure Optimization**
- **CDN** - CloudFlare, AWS CloudFront
- **Load Balancer** - Multiple backend instances
- **Database** - PostgreSQL with connection pooling
- **Caching** - Redis for API responses

---

## 📋 **Deployment Checklist**

### **Pre-Deployment**
- [ ] Environment variables configured
- [ ] API keys added and tested
- [ ] Domain DNS configured
- [ ] SSL certificate obtained
- [ ] Backup strategy in place

### **Deployment**
- [ ] Build and test locally
- [ ] Deploy to staging first
- [ ] Run health checks
- [ ] Monitor logs for errors
- [ ] Test all functionality

### **Post-Deployment**
- [ ] Monitor performance metrics
- [ ] Set up alerts and monitoring
- [ ] Document deployment process
- [ ] Plan rollback strategy
- [ ] Schedule regular updates

---

## 🆘 **Troubleshooting**

### **Common Issues**

**Backend not starting:**
```bash
# Check logs
docker-compose logs backend

# Common fixes
- Verify API keys in .env
- Check port conflicts
- Ensure dependencies installed
```

**Frontend build fails:**
```bash
# Check Node.js version
node --version  # Should be 16+

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**SSL certificate issues:**
```bash
# Renew certificate
sudo certbot renew

# Check certificate status
sudo certbot certificates
```

### **Support Commands**
```bash
# Full system restart
./deploy.sh down && ./deploy.sh production

# View resource usage
docker stats

# Clean up space
docker system prune -a
```

---

## 🎉 **Success!**

Your PitchOS application is now deployed and ready for production use!

**Access Points:**
- 🌐 **Frontend**: https://your-domain.com
- 🔧 **API**: https://your-domain.com/api
- 📚 **API Docs**: https://your-domain.com/docs

**Next Steps:**
1. Set up monitoring and alerts
2. Configure automated backups
3. Plan scaling strategy
4. Monitor user feedback and performance

**Need Help?**
- Check logs: `docker-compose logs -f`
- Health check: `curl https://your-domain.com/health`
- Restart services: `./deploy.sh restart`
