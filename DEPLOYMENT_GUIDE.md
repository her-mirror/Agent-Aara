# 🚀 Aara Health Agent - Next.js Integration & Deployment Guide

This guide will help you host and integrate your Aara Health Agent with a Next.js frontend application.

## 📋 Overview

Your integration will have two main components:
1. **FastAPI Backend** - Python-based AI agent serving API endpoints
2. **Next.js Frontend** - React-based web application for user interaction

## 🔧 Phase 1: Backend API Setup

### 1. Install Additional Dependencies

```bash
# Install FastAPI dependencies
pip install fastapi uvicorn[standard] pydantic

# Or update requirements.txt and reinstall
pip install -r requirements.txt
```

### 2. Start the API Server

```bash
# Option 1: Using the new API script
python scripts/run_api.py

# Option 2: Direct FastAPI run
python api/main.py

# Option 3: Using uvicorn directly
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Test the API

```bash
# Health check
curl http://localhost:8000/health

# Chat endpoint test
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello Aara!"}'
```

## 🎨 Phase 2: Frontend Setup

### 1. Create Next.js Application

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Or if you prefer yarn
yarn install
```

### 2. Environment Configuration

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Aara Health Agent
NEXT_PUBLIC_APP_VERSION=1.0.0
```

### 3. Start Development Server

```bash
# In the frontend directory
npm run dev

# Or with yarn
yarn dev
```

## 🐳 Phase 3: Docker Deployment

### 1. Full Stack Docker Setup

Create `docker-compose.full.yml`:

```yaml
version: '3.8'
services:
  Aara-api:
    build: .
    container_name: Aara-api
    env_file:
      - .env
    volumes:
      - ./data:/app/data
    working_dir: /app
    command: ["python", "api/main.py"]
    ports:
      - "8000:8000"
    networks:
      - Aara-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  Aara-frontend:
    build: ./frontend
    container_name: Aara-frontend
    environment:
      - NEXT_PUBLIC_API_URL=http://Aara-api:8000
    ports:
      - "3000:3000"
    depends_on:
      - Aara-api
    networks:
      - Aara-network

networks:
  Aara-network:
    driver: bridge
```

### 2. Frontend Dockerfile

Create `frontend/Dockerfile`:

```dockerfile
FROM node:18-alpine AS base

# Install dependencies only when needed
FROM base AS deps
WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./
RUN npm ci

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build the application
RUN npm run build

# Production image
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public

# Copy built application
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000

CMD ["node", "server.js"]
```

### 3. Build and Run

```bash
# Build and run the full stack
docker-compose -f docker-compose.full.yml up --build

# Or run in detached mode
docker-compose -f docker-compose.full.yml up -d --build
```

## ☁️ Phase 4: Cloud Deployment

### Option 1: Vercel + Railway

#### Backend (Railway)
1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy the backend using the existing Dockerfile

#### Frontend (Vercel)
1. Connect your GitHub repository to Vercel
2. Set the frontend directory as the root
3. Configure environment variables:
   - `NEXT_PUBLIC_API_URL=https://your-railway-app.railway.app`

### Option 2: DigitalOcean App Platform

Create `frontend/.do/app.yaml`:

```yaml
name: Aara-health-agent
services:
- name: Aara-api
  source_dir: /
  dockerfile_path: Dockerfile
  github:
    repo: your-username/Aara-health-agent
    branch: main
  http_port: 8000
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: OPENAI_API_KEY
    value: your-openai-key
    type: SECRET
  - key: TAVILY_API_KEY
    value: your-tavily-key
    type: SECRET

- name: Aara-frontend
  source_dir: /frontend
  dockerfile_path: frontend/Dockerfile
  github:
    repo: your-username/Aara-health-agent
    branch: main
  http_port: 3000
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: NEXT_PUBLIC_API_URL
    value: ${Aara-api.PUBLIC_URL}
```

### Option 3: AWS ECS with ALB

1. **Create ECR repositories** for both services
2. **Build and push images**:
   ```bash
   # Build and push backend
   docker build -t Aara-api .
   docker tag Aara-api:latest your-account.dkr.ecr.region.amazonaws.com/Aara-api:latest
   docker push your-account.dkr.ecr.region.amazonaws.com/Aara-api:latest

   # Build and push frontend
   docker build -t Aara-frontend ./frontend
   docker tag Aara-frontend:latest your-account.dkr.ecr.region.amazonaws.com/Aara-frontend:latest
   docker push your-account.dkr.ecr.region.amazonaws.com/Aara-frontend:latest
   ```

3. **Create ECS services** with Application Load Balancer
4. **Configure environment variables** in ECS task definitions

## 🔐 Phase 5: Security & Production Setup

### 1. Environment Variables

**Backend (.env):**
```env
OPENAI_API_KEY=your-openai-key
TAVILY_API_KEY=your-tavily-key
ENVIRONMENT=production
LOG_LEVEL=INFO
CORS_ORIGINS=https://your-frontend-domain.com
```

**Frontend (.env.production):**
```env
NEXT_PUBLIC_API_URL=https://your-backend-domain.com
NEXT_PUBLIC_APP_NAME=Aara Health Agent
NEXT_PUBLIC_ENVIRONMENT=production
```

### 2. CORS Configuration

Update `api/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],  # Update with your domain
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### 3. HTTPS & SSL

- Use Let's Encrypt for SSL certificates
- Configure reverse proxy with Nginx if needed
- Enable HSTS headers

## 📊 Phase 6: Monitoring & Analytics

### 1. Health Checks

The API includes health check endpoints:
- `GET /health` - Basic health status
- `GET /` - API information

### 2. Logging

Configure structured logging in production:

```python
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
```

### 3. Error Tracking

Consider integrating:
- Sentry for error tracking
- DataDog for APM
- CloudWatch for AWS deployments

## 🚀 Quick Start Commands

### Local Development
```bash
# Terminal 1: Start backend
python scripts/run_api.py

# Terminal 2: Start frontend
cd frontend && npm run dev

# Open http://localhost:3000
```

### Docker Development
```bash
# Full stack with docker-compose
docker-compose -f docker-compose.full.yml up --build

# Open http://localhost:3000
```

### Production Build
```bash
# Build frontend for production
cd frontend && npm run build

# Start production backend
python api/main.py

# Start production frontend
cd frontend && npm start
```

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| POST | `/chat` | Send message to Aara |
| GET | `/conversations/{id}` | Get conversation history |
| DELETE | `/conversations/{id}` | Delete conversation |

## 📱 Frontend Features

- **Responsive Design** - Works on desktop and mobile
- **Real-time Chat** - Instant messaging with Aara
- **Message History** - Conversation persistence
- **Loading States** - Visual feedback during AI processing
- **Error Handling** - Graceful error management
- **Markdown Support** - Rich text formatting in responses

## 🛟 Troubleshooting

### Common Issues

1. **CORS Error**: Update allowed origins in `api/main.py`
2. **API Connection Failed**: Check `NEXT_PUBLIC_API_URL` in frontend
3. **Import Errors**: Ensure all dependencies are installed
4. **Docker Issues**: Check port conflicts and environment variables

### Debug Commands

```bash
# Check API status
curl http://localhost:8000/health

# Check frontend build
cd frontend && npm run build

# View API logs
docker logs Aara-api

# View frontend logs
docker logs Aara-frontend
```

## 📈 Performance Optimization

1. **Backend Optimization**:
   - Use async FastAPI routes
   - Implement response caching
   - Optimize database queries

2. **Frontend Optimization**:
   - Enable Next.js Image optimization
   - Use dynamic imports for code splitting
   - Implement service worker for caching

3. **Database Optimization**:
   - Consider PostgreSQL for production
   - Implement connection pooling
   - Use Redis for session storage

## 🎯 Next Steps

1. **Deploy to staging environment**
2. **Set up CI/CD pipeline**
3. **Configure monitoring and alerts**
4. **Implement user authentication**
5. **Add conversation export features**
6. **Set up automated testing**

---

🌸 **Happy Deploying!** Your Aara Health Agent is now ready to help users with their health and wellness questions through a beautiful, modern web interface. 