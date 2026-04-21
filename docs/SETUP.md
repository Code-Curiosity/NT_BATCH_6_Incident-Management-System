# Local Development Setup

## Prerequisites
- Python 3.10+
- Node.js 18+
- MySQL 8.0+

## 1. Database Setup
```sql
CREATE DATABASE incident_management;
```

## 2. Backend Setup
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt

# Copy and configure environment
copy .env.example .env
# Edit .env with your MySQL credentials

# Run server
uvicorn main:app --reload --port 8000
```

## 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 4. Access
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs (Swagger): http://localhost:8000/docs

## 5. Test Alert Ingestion
```bash
python scripts/simulate_alerts.py
```
