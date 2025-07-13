# Backend Architecture

This backend follows a modular, layered architecture designed for scalability and maintainability.

## 📁 Directory Structure

```
backend/
├── api/                    # 🚀 API Layer
│   ├── __init__.py
│   ├── app.py             # FastAPI application factory
│   └── routes/            # Route handlers
│       ├── __init__.py
│       ├── stories.py     # Story endpoints
│       ├── analytics.py   # Analytics endpoints
│       └── tasks.py       # Task endpoints
├── core/                  # ⚙️ Core Configuration
│   ├── __init__.py
│   ├── config.py          # Application settings
│   └── celery_app.py      # Celery configuration
├── database/              # 🗄️ Database Layer
│   ├── __init__.py
│   ├── models.py          # SQLAlchemy models
│   ├── crud.py            # Database operations
│   └── database.py        # Database connection
├── services/              # 🔧 Business Logic
│   ├── __init__.py
│   ├── hn_service.py      # Hacker News API service
│   ├── analytics_service.py # Analytics processing
│   └── redis_service.py   # Redis messaging
├── tasks/                 # ⚡ Background Tasks
│   ├── __init__.py
│   └── story_tasks.py     # Celery tasks
├── schemas/               # 📋 Data Schemas
│   ├── __init__.py
│   ├── story.py           # Story schemas
│   ├── analytics.py       # Analytics schemas
│   └── responses.py       # Response schemas
└── workers/               # 🔄 Background Workers
    ├── __init__.py
    └── background_processor.py # Redis event processor
```

## 🏗️ Architecture Layers

### 1. **API Layer** (`api/`)
- **Purpose**: HTTP interface and request handling
- **Components**: FastAPI app, route handlers, middleware
- **Responsibilities**: Request validation, response formatting, CORS

### 2. **Core Layer** (`core/`)
- **Purpose**: Application configuration and utilities
- **Components**: Settings, Celery config, shared utilities
- **Responsibilities**: Environment management, app configuration

### 3. **Database Layer** (`database/`)
- **Purpose**: Data persistence and access
- **Components**: Models, CRUD operations, connection management
- **Responsibilities**: Data storage, querying, migrations

### 4. **Services Layer** (`services/`)
- **Purpose**: Business logic and external integrations
- **Components**: HN API, analytics processing, Redis messaging
- **Responsibilities**: Data processing, external API calls

### 5. **Tasks Layer** (`tasks/`)
- **Purpose**: Background job processing
- **Components**: Celery tasks for async operations
- **Responsibilities**: Story fetching, analytics processing

### 6. **Schemas Layer** (`schemas/`)
- **Purpose**: Data validation and serialization
- **Components**: Pydantic models for request/response
- **Responsibilities**: Input validation, output formatting

### 7. **Workers Layer** (`workers/`)
- **Purpose**: Background event processing
- **Components**: Redis event handlers
- **Responsibilities**: Event-driven processing

## 🔄 Data Flow

1. **Request** → API Layer (validation)
2. **API Layer** → Services Layer (business logic)
3. **Services Layer** → Database Layer (data access)
4. **Database Layer** → Services Layer (data return)
5. **Services Layer** → API Layer (response formatting)
6. **API Layer** → Client (response)

## 🚀 Benefits

- **Separation of Concerns**: Each layer has a specific responsibility
- **Testability**: Easy to mock dependencies and test in isolation
- **Maintainability**: Clear structure makes code easy to navigate
- **Scalability**: Can easily add new services, tasks, or endpoints
- **Reusability**: Services can be used by multiple endpoints

## 📝 Adding New Features

### New API Endpoint
1. Add route in `api/routes/`
2. Add schema in `schemas/`
3. Add service method in `services/`
4. Add CRUD operations in `database/`

### New Background Task
1. Add task in `tasks/`
2. Update Celery config in `core/celery_app.py`
3. Add route to trigger task in `api/routes/tasks.py`

### New Service
1. Create service in `services/`
2. Add configuration in `core/config.py`
3. Import and use in routes or tasks 