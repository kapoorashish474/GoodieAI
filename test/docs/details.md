# Docker Services: Testing & Database Verification

## 1. Testing All Docker Services Are Working

To ensure all services (PostgreSQL, Redis, Backend, Celery Worker, Frontend) are running and healthy:

### Step 1: Start All Services
```bash
docker-compose up --build
```
- This will build and start all containers as defined in `docker-compose.yml`.

### Step 2: Check Service Health
- **Docker Compose Output:**
  - Look for `healthy` status in the logs for `postgres` and `redis`.
  - Ensure there are no errors for `backend`, `celery-worker`, or `frontend`.
- **List Running Containers:**
```bash
docker-compose ps
```
  - All services should show `Up` (and `healthy` for those with healthchecks).

### Step 3: Test Service Endpoints
- **Backend API:**
  - Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser. You should see the FastAPI docs.
- **Frontend:**
  - Open [http://localhost:3000](http://localhost:3000) in your browser. The dashboard UI should load.
- **Database:**
  - The database should be accessible on port 5432.
- **Redis:**
  - Redis should be accessible on port 6379.

## 2. Connecting to the Database & Checking Tables

You can connect to the running PostgreSQL container to inspect tables:

### Option A: Using psql from Host (if installed)
```bash
psql -h localhost -U ashishkapoor -d hn_analytics
```
- Password: `password` (default, unless changed in your `.env`)

### Option B: Using psql Inside the Container
```bash
docker-compose exec postgres psql -U ashishkapoor -d hn_analytics
```

### List All Tables
Once in the `psql` prompt, run:
```sql
\dt
```
- This will show all tables in the current database.

### Describe a Table
To see the schema for a table (e.g., `stories`):
```sql
\d stories
```

---

**Note:**
- Default credentials are set in `docker-compose.yml` and can be overridden by environment variables or `.env` file.
- If you have changed the database name, user, or password, use those values instead.
- For more advanced database inspection, you can use GUI tools like DBeaver or TablePlus and connect to `localhost:5432` with the same credentials.
