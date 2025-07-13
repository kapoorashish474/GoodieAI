# 🚀 Real-Time Hacker News Analytics Dashboard

A full-stack web application that fetches top Hacker News stories, processes them for AI-related trends and brand mentions, and displays analytics in a modern dashboard interface.

## ✨ Features

- **📊 Real-time Analytics**: Track AI-related keywords and domain trends
- **🔍 Story Explorer**: Search and filter through HN stories
- **📈 Interactive Dashboard**: Beautiful charts and visualizations
- **⚡ Background Processing**: Asynchronous story processing with Celery
- **🔄 Event-Driven Architecture**: Redis-based messaging system
- **🎯 Modular Design**: Scalable, maintainable codebase

## 🐳 **Docker IS Included in the Project**

The project has complete Docker support with:

1. **`docker-compose.yml`** - Orchestrates all services
2. **`Dockerfile`** - Backend container
3. **`frontend/Dockerfile`** - Frontend container

### **Current Docker Services:**
- PostgreSQL Database
- Redis Cache/Queue  
- Backend API (FastAPI)
- Celery Worker
- Frontend (Next.js)

## 🔧 **Why Docker Should Be in the Architecture**

Docker provides several benefits that should be highlighted:

1. **Consistency**: Same environment across development/production
2. **Isolation**: Services don't interfere with each other
3. **Scalability**: Easy to scale individual services
4. **Deployment**: One command to run everything
5. **Dependencies**: No need to install PostgreSQL/Redis locally

## 📊 **Updated Architecture Diagram**

The architecture should include Docker as an **orchestration layer**:

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Compose                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Frontend      │  │   Backend API   │  │   Background    │ │
│  │   (Next.js)     │◄─┤   (FastAPI)     │◄─┤   Processor     │ │
│  │   Container     │  │   Container     │  │   (Celery)      │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│           │                       │                       │   │
│           └───────────────────────┼───────────────────────┘   │
│                                   │                           │
│  ┌─────────────────┐  ┌─────────────────┐                    │
│  │   PostgreSQL    │  │     Redis       │                    │
│  │   Container     │  │   Container     │                    │
│  └─────────────────┘  └─────────────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **PostgreSQL**
- **Redis**

### Installation

1. **Clone and setup:**
   ```bash
   cd startup/test
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Frontend setup:**
   ```bash
   cd frontend
   npm install
   ```

3. **Environment configuration:**
   ```bash
   # Copy the example environment file
   cp env.example .env
   
   # Edit .env with your actual values
   # Never commit .env files to version control
   ```
   
   Example `.env` file:
   ```env
   # Database
   DATABASE_URL=postgresql://username:password@localhost:5432/hn_analytics
   POSTGRES_DB=hn_analytics
   POSTGRES_USER=your_username
   POSTGRES_PASSWORD=your_secure_password
   
   # Redis
   REDIS_URL=redis://localhost:6379
   
   # Hacker News API
   HN_API_BASE_URL=https://hacker-news.firebaseio.com/v0
   HN_TOP_STORIES_LIMIT=50
   
   # Application
   APP_NAME=Hacker News Analytics Dashboard
   DEBUG=false
   
   # Frontend
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. **Database setup:**
   ```bash
   createdb hn_analytics
   python main.py create-tables
   ```

### Running the Application

#### Backend Services

1. **API Server:**
   ```bash
   python main.py api --reload
   ```
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs

2. **Celery Worker:**
   ```bash
   python main.py celery-worker
   ```

3. **Background Processor (optional):**
   ```bash
   python main.py processor
   ```

#### Frontend

```bash
cd frontend
npm run dev
```
- Frontend: http://localhost:3000

## 📊 Dashboard Features

### **Analytics Dashboard**
- 📈 Keyword frequency charts
- 🌐 Top domains visualization
- 📊 Story statistics
- ⏰ Real-time data updates

### **Story Explorer**
- 🔍 Advanced search and filtering
- 📋 Sortable data tables
- 🔗 Direct links to HN stories
- 📱 Responsive design

## 🔧 API Endpoints

### Core Endpoints
- `GET /` - API information
- `GET /health` - Health check
- `GET /dashboard` - Dashboard data

### Stories
- `GET /api/v1/stories` - Get stories with pagination
- `GET /api/v1/stories/{id}` - Get specific story
- `POST /api/v1/fetch-stories` - Fetch new stories

### Analytics
- `GET /api/v1/analytics` - Get keyword analytics
- `GET /api/v1/domains` - Get domain analytics

### Tasks
- `POST /api/v1/tasks/fetch-stories` - Trigger story fetching
- `GET /api/v1/tasks/{id}` - Get task status

## 🧪 Testing

### Quick Test Runner
```bash
# Run all tests
python3 run_tests.py all

# Run specific test types
python3 run_tests.py unit        # Unit tests only
python3 run_tests.py integration # Integration tests only
python3 run_tests.py e2e         # End-to-end tests only
python3 run_tests.py coverage    # With coverage report
```

### Manual Test Execution
```bash
# Backend tests
python3 tests/integration/test_backend.py

# E2E tests
python3 tests/e2e/test_e2e.py

# Pytest tests
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

For detailed testing information, see [tests/README.md](./tests/README.md).

## 📁 Project Structure

```
startup/test/
├── backend/                 # 🐍 Backend (FastAPI + Celery)
│   ├── api/                # API layer
│   ├── core/               # Configuration
│   ├── database/           # Database models & CRUD
│   ├── services/           # Business logic
│   ├── tasks/              # Background tasks
│   ├── schemas/            # Pydantic schemas
│   └── workers/            # Background workers
├── frontend/               # ⚛️ Frontend (Next.js)
│   ├── src/
│   │   ├── app/           # App router pages
│   │   ├── components/    # React components
│   │   └── lib/           # Utilities & API client
│   └── public/            # Static assets
├── tests/                  # 🧪 Test Suite
│   ├── unit/              # Unit tests (pytest)
│   ├── integration/       # Integration tests
│   ├── e2e/              # End-to-end tests
│   ├── conftest.py       # Pytest configuration
│   └── README.md         # Test documentation
├── docs/                  # 📚 Documentation
├── run_tests.py          # Test runner script
├── pytest.ini           # Pytest configuration
└── requirements.txt      # Python dependencies
```

## 🔄 Data Flow

1. **Story Ingestion:**
   - Celery task fetches top HN stories
   - Stores in PostgreSQL database
   - Publishes events to Redis

2. **Analytics Processing:**
   - Background processor analyzes stories
   - Extracts AI keywords and domains
   - Updates analytics tables

3. **Frontend Display:**
   - React components fetch data via API
   - Recharts renders visualizations
   - Real-time updates via polling

## 🚨 Troubleshooting

### Common Issues

1. **Virtual Environment:**
   ```bash
   # Ensure you're in the right directory
   cd /Users/ashishkapoor/Workspace/startup/test
   source venv/bin/activate
   ```

2. **Database Connection:**
   ```bash
   # Check PostgreSQL is running
   brew services start postgresql
   
   # Create database if needed
   createdb hn_analytics
   ```

3. **Redis Connection:**
   ```bash
   # Start Redis
   brew services start redis
   ```

4. **Port Conflicts:**
   - Backend: Change port in `main.py`
   - Frontend: Change port in `package.json`

### Debug Mode

Enable debug mode in `.env`:
```env
DEBUG=true
```

## 🔮 Future Enhancements

- [ ] **Real-time Updates**: WebSocket integration
- [ ] **Authentication**: User login and authorization
- [ ] **Caching**: Redis caching layer
- [ ] **Rate Limiting**: API rate limiting
- [ ] **Docker**: Containerization
- [ ] **CI/CD**: GitHub Actions pipeline
- [ ] **Monitoring**: Health checks and metrics
- [ ] **Multi-source**: Reddit, Twitter integration

## 🔒 Security

This project follows security best practices:

- ✅ **Environment Variables**: All sensitive configuration uses environment variables
- ✅ **No Hardcoded Secrets**: No passwords or API keys in source code
- ✅ **Protected Files**: `.env` files and build artifacts are gitignored
- ✅ **Docker Security**: Container configuration uses environment variables

For detailed security information, see [SECURITY.md](./SECURITY.md).

### Quick Security Setup
```bash
# 1. Copy environment template
cp env.example .env

# 2. Edit with secure values
nano .env

# 3. Never commit .env files
git add .gitignore
git commit -m "Add security: gitignore sensitive files"
```

## 📝 Development

### Adding New Features

1. **Backend API:**
   - Add route in `backend/api/routes/`
   - Add schema in `backend/schemas/`
   - Add service in `backend/services/`

2. **Frontend:**
   - Add page in `frontend/src/app/`
   - Add component in `frontend/src/components/`
   - Update API client in `frontend/src/lib/`

### Code Style

- **Backend**: Follow PEP 8, use type hints
- **Frontend**: Use TypeScript, follow ESLint rules
- **Commits**: Use conventional commit messages

## 📄 License

This project is part of a system design implementation for educational purposes.

---

**Built with ❤️ using FastAPI, Next.js, and modern web technologies**
