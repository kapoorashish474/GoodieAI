# Sequence Diagram: Hacker News Analytics Dashboard

## 🔄 Complete Application Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    User     │    │  Frontend   │    │ Backend API │    │   Celery    │    │ HN API      │
│             │    │  (Next.js)  │    │  (FastAPI)  │    │   Worker    │    │             │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │                  │                  │
       │ 1. Access        │                  │                  │                  │
       │ Dashboard        │                  │                  │                  │
       │ ────────────────▶│                  │                  │                  │
       │                  │ 2. GET /dashboard│                  │                  │
       │                  │ ────────────────▶│                  │                  │
       │                  │                  │ 3. Query DB      │                  │
       │                  │                  │ ────────────────▶│                  │
       │                  │                  │                  │                  │
       │                  │                  │ 4. Return data   │                  │
       │                  │                  │ ◀────────────────│                  │
       │                  │ 5. Dashboard data│                  │                  │
       │                  │ ◀────────────────│                  │                  │
       │ 6. Render charts │                  │                  │                  │
       │ ◀────────────────│                  │                  │                  │
       │                  │                  │                  │                  │
       │ 7. Click "Fetch  │                  │                  │                  │
       │ Stories"         │                  │                  │                  │
       │ ────────────────▶│                  │                  │                  │
       │                  │ 8. POST /tasks/  │                  │                  │
       │                  │ fetch-stories    │                  │                  │
       │                  │ ────────────────▶│                  │                  │
       │                  │                  │ 9. Trigger task  │                  │
       │                  │                  │ ────────────────▶│                  │
       │                  │                  │                  │ 10. GET /topstories│
       │                  │                  │                  │ ────────────────▶│
       │                  │                  │                  │                  │
       │                  │                  │                  │ 11. Story IDs    │
       │                  │                  │                  │ ◀────────────────│
       │                  │                  │                  │                  │
       │                  │                  │                  │ 12. GET /item/{id}│
       │                  │                  │                  │ ────────────────▶│
       │                  │                  │                  │                  │
       │                  │                  │                  │ 13. Story details│
       │                  │                  │                  │ ◀────────────────│
       │                  │                  │                  │                  │
       │                  │                  │ 14. Store story  │                  │
       │                  │                  │ ◀────────────────│                  │
       │                  │                  │                  │                  │
       │                  │                  │ 15. Task status  │                  │
       │                  │                  │ ────────────────▶│                  │
       │                  │ 16. Task started │                  │                  │
       │                  │ ◀────────────────│                  │                  │
       │ 17. Show status  │                  │                  │                  │
       │ ◀────────────────│                  │                  │                  │
       │                  │                  │                  │                  │
       │ 18. Poll status  │                  │                  │                  │
       │ ────────────────▶│                  │                  │                  │
       │                  │ 19. GET /tasks/  │                  │                  │
       │                  │ {task_id}        │                  │                  │
       │                  │ ────────────────▶│                  │                  │
       │                  │                  │ 20. Check status │                  │
       │                  │                  │ ────────────────▶│                  │
       │                  │                  │                  │                  │
       │                  │                  │ 21. Task progress│                  │
       │                  │                  │ ◀────────────────│                  │
       │                  │ 22. Status update│                  │                  │
       │                  │ ◀────────────────│                  │                  │
       │ 23. Update UI    │                  │                  │                  │
       │ ◀────────────────│                  │                  │                  │
       │                  │                  │                  │                  │
       │ 24. Refresh data │                  │                  │                  │
       │ ────────────────▶│                  │                  │                  │
       │                  │ 25. GET /dashboard│                  │                  │
       │                  │ ────────────────▶│                  │                  │
       │                  │                  │ 26. Query updated│                  │
       │                  │                  │ data             │                  │
       │                  │                  │ ────────────────▶│                  │
       │                  │                  │                  │                  │
       │                  │                  │ 27. Latest data  │                  │
       │                  │                  │ ◀────────────────│                  │
       │                  │ 28. Updated      │                  │                  │
       │                  │ dashboard        │                  │                  │
       │                  │ ◀────────────────│                  │                  │
       │ 29. New charts   │                  │                  │                  │
       │ ◀────────────────│                  │                  │                  │
```

## 📊 Background Processing Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Celery    │    │    Redis    │    │ Background  │    │ PostgreSQL  │
│   Worker    │    │   Events    │    │ Processor   │    │  Database   │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │                  │
       │ 1. Process story │                  │                  │
       │ ────────────────▶│                  │                  │
       │                  │                  │                  │
       │                  │ 2. Publish event │                  │
       │                  │ ────────────────▶│                  │
       │                  │                  │                  │
       │                  │ 3. Story event   │                  │
       │                  │ ◀────────────────│                  │
       │                  │                  │                  │
       │                  │                  │ 4. Extract       │                  │
       │                  │                  │ keywords         │                  │
       │                  │                  │ ────────────────▶│                  │
       │                  │                  │                  │
       │                  │                  │ 5. Update        │                  │
       │                  │                  │ analytics        │                  │
       │                  │                  │ ────────────────▶│                  │
       │                  │                  │                  │
       │                  │                  │ 6. Analytics     │                  │
       │                  │                  │ updated          │                  │
       │                  │                  │ ◀────────────────│                  │
```

## 🔍 Story Explorer Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    User     │    │  Frontend   │    │ Backend API │
│             │    │  (Next.js)  │    │  (FastAPI)  │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
       │ 1. Navigate to   │                  │
       │ Explorer         │                  │
       │ ────────────────▶│                  │
       │                  │ 2. GET /stories  │                  │
       │                  │ ────────────────▶│                  │
       │                  │                  │ 3. Query stories │                  │
       │                  │                  │ ────────────────▶│                  │
       │                  │                  │                  │
       │                  │                  │ 4. Story list    │                  │
       │                  │                  │ ◀────────────────│                  │
       │                  │ 5. Stories data  │                  │
       │                  │ ◀────────────────│                  │
       │ 6. Display table │                  │                  │
       │ ◀────────────────│                  │                  │
       │                  │                  │                  │
       │ 7. Apply filters │                  │                  │
       │ ────────────────▶│                  │                  │
       │                  │ 8. GET /stories  │                  │
       │                  │ with filters     │                  │
       │                  │ ────────────────▶│                  │
       │                  │                  │ 9. Filtered query│                  │
       │                  │                  │ ────────────────▶│                  │
       │                  │                  │                  │
       │                  │                  │ 10. Filtered     │                  │
       │                  │                  │ results          │                  │
       │                  │                  │ ◀────────────────│                  │
       │                  │ 11. Filtered     │                  │
       │                  │ stories          │                  │
       │                  │ ◀────────────────│                  │
       │ 12. Updated table│                  │                  │
       │ ◀────────────────│                  │                  │
```

## 📈 Analytics API Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Frontend   │    │ Backend API │    │ PostgreSQL  │    │   Charts    │
│  (Next.js)  │    │  (FastAPI)  │    │  Database   │    │ (Recharts)  │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │                  │
       │ 1. GET /analytics│                  │                  │
       │ ────────────────▶│                  │                  │
       │                  │ 2. Query keywords│                  │
       │                  │ ────────────────▶│                  │
       │                  │                  │                  │
       │                  │ 3. Keyword data  │                  │
       │                  │ ◀────────────────│                  │
       │ 4. Analytics data│                  │                  │
       │ ◀────────────────│                  │                  │
       │                  │                  │                  │
       │ 5. GET /domains  │                  │                  │
       │ ────────────────▶│                  │                  │
       │                  │ 6. Query domains │                  │
       │                  │ ────────────────▶│                  │
       │                  │                  │                  │
       │                  │ 7. Domain data   │                  │
       │                  │ ◀────────────────│                  │
       │ 8. Domain data   │                  │                  │
       │ ◀────────────────│                  │                  │
       │                  │                  │                  │
       │ 9. Render charts │                  │                  │
       │ ────────────────▶│                  │                  │
       │                  │                  │                  │
       │ 10. Visual charts│                  │                  │
       │ ◀────────────────│                  │                  │
```

## 🔄 Scheduled Background Processing

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Celery    │    │ HN API      │    │ PostgreSQL  │    │ Background  │
│   Beat      │    │             │    │  Database   │    │ Processor   │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │                  │
       │ 1. Every 30 min  │                  │                  │
       │ ────────────────▶│                  │                  │
       │                  │                  │                  │
       │                  │ 2. GET /topstories│                  │
       │                  │ ────────────────▶│                  │
       │                  │                  │                  │
       │                  │ 3. Latest IDs    │                  │
       │                  │ ◀────────────────│                  │
       │                  │                  │                  │
       │ 4. Check for new │                  │                  │
       │ stories          │                  │                  │
       │ ────────────────▶│                  │                  │
       │                  │                  │                  │
       │ 5. New stories   │                  │                  │
       │ found            │                  │                  │
       │ ◀────────────────│                  │                  │
       │                  │                  │                  │
       │ 6. Process new   │                  │                  │
       │ stories          │                  │                  │
       │ ────────────────▶│                  │                  │
       │                  │                  │                  │
       │ 7. Analytics     │                  │                  │
       │ updated          │                  │                  │
       │ ◀────────────────│                  │                  │
```

## 📋 Component Descriptions

### **User Interface Layer**
- **Frontend (Next.js)**: React components with TypeScript
- **Pages**: Dashboard, Explorer, Navigation
- **Components**: Charts (Recharts), Tables, Forms
- **State Management**: React hooks for data fetching

### **API Gateway Layer**
- **FastAPI**: RESTful API with OpenAPI documentation
- **Routes**: Stories, Analytics, Tasks, Health
- **Middleware**: CORS, request validation
- **Response**: JSON with proper HTTP status codes

### **Background Processing Layer**
- **Celery**: Asynchronous task queue
- **Tasks**: Story fetching, analytics processing
- **Redis**: Message broker and result backend
- **Workers**: Scalable background processing

### **Data Processing Layer**
- **Analytics Service**: Keyword extraction, domain analysis
- **HN Service**: External API integration
- **Background Processor**: Event-driven processing
- **Data Transformation**: Raw data to analytics

### **Data Persistence Layer**
- **PostgreSQL**: Primary database
- **Models**: Stories, Analytics, Domains
- **CRUD Operations**: Database interactions
- **Migrations**: Schema management

## 🎯 Key Benefits

- **Asynchronous Processing**: Non-blocking user experience
- **Event-Driven**: Real-time updates via Redis
- **Scalable**: Celery workers can be scaled horizontally
- **Modular**: Each component has a single responsibility
- **Reliable**: Redis provides message persistence
- **Real-time**: Frontend polls for updates
- **Extensible**: Easy to add new data sources 