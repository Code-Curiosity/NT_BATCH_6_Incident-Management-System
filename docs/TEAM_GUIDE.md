# 🚨 Team Guide — Incident Management System

> **Read this FULLY before writing a single line of code.**
> This is a hackathon (18 hrs). We cannot waste time on confusion or conflicts.

---

## 📍 Quick Links

| What | Link |
|------|------|
| GitHub Repo | https://github.com/Code-Curiosity/NT_BATCH_6_Incident-Management-System |
| Main Branch (stable) | `main` — DO NOT push directly |
| Dev Branch (integration) | `dev` — DO NOT push directly |
| Your Branch | `feature/your-task-name` |

---

## 🖥️ How This Works (Remote Team)

We are all working from different locations. Here's how we stay in sync:

### Code → GitHub
- Everyone clones the same repo
- Everyone works on their **own feature branch**
- You push your branch → create a **Pull Request (PR)** → team lead reviews and merges

### Database → Each Person Runs Their Own
- **You do NOT share a database**
- Each person runs a **local SQLite database** on their own machine (zero setup needed)
- The code auto-creates a `incidents.db` file in the `backend/` folder
- For the final demo, the team lead will switch to MySQL if needed

### Frontend & Backend → Both Run Locally
- Backend runs on `http://localhost:8000`
- Frontend runs on `http://localhost:5173`
- Vite auto-proxies `/api/*` calls to the backend — so it just works

### No Cloud Server Needed During Development
- Everything runs on your laptop
- No hosting, no deployment, no cloud DB during development

---

## 💻 First-Time Setup (EVERY TEAMMATE MUST DO THIS)

### Step 1: Clone the repo
```bash
git clone https://github.com/Code-Curiosity/NT_BATCH_6_Incident-Management-System.git
cd NT_BATCH_6_Incident-Management-System
```

### Step 2: Switch to dev branch
```bash
git checkout dev
git pull origin dev
```

### Step 3: Create your feature branch
```bash
git checkout -b feature/your-task-name
```

Examples:
- `feature/backend-api` 
- `feature/frontend-dashboard`
- `feature/classification-engine`
- `feature/websocket-realtime`
- `feature/alert-simulator`

### Step 4: Setup Backend
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### Step 5: Create your .env file
```bash
# Copy the example
# Windows:
copy .env.example .env
# Mac/Linux:
cp .env.example .env
```

Edit `.env` file and set:
```
DATABASE_URL=sqlite:///./incidents.db
APP_ENV=development
DEBUG=true
```

> ⚠️ Use the SQLite URL above. Do NOT use MySQL for local development.

### Step 6: Run Backend
```bash
uvicorn main:app --reload --port 8000
```

✅ Check: Open `http://localhost:8000/docs` — you should see Swagger API docs.

### Step 7: Setup Frontend (in a new terminal)
```bash
cd frontend
npm install
npm run dev
```

✅ Check: Open `http://localhost:5173` — you should see the dashboard.

### Step 8: Test with sample alerts
```bash
# In a third terminal, from project root
cd backend
# Activate venv first
python ../scripts/simulate_alerts.py
```

---

## 📁 Project Structure — WHO WORKS WHERE

```
incident-management-system/
│
├── backend/                    ← BACKEND TEAM ONLY
│   ├── app/
│   │   ├── routes/
│   │   │   ├── incidents.py    ← Incident CRUD API endpoints
│   │   │   ├── alerts.py       ← Alert ingestion endpoint
│   │   │   └── websocket.py    ← WebSocket real-time connection
│   │   ├── models/
│   │   │   └── incident.py     ← Database model (table schema)
│   │   ├── services/
│   │   │   ├── classification.py ← Alert classification logic
│   │   │   └── notification.py   ← Notification stubs (email/Slack)
│   │   └── database.py         ← DB connection config
│   ├── main.py                 ← FastAPI app entry point
│   └── requirements.txt        ← Python dependencies
│
├── frontend/                   ← FRONTEND TEAM ONLY
│   ├── src/
│   │   ├── components/
│   │   │   ├── IncidentCard.jsx + .css   ← Single incident card
│   │   │   └── StatsBar.jsx + .css       ← Stats overview bar
│   │   ├── pages/
│   │   │   └── Dashboard.jsx + .css      ← Main dashboard page
│   │   ├── App.jsx             ← Router setup
│   │   ├── main.jsx            ← React entry point
│   │   └── index.css           ← Global styles & design tokens
│   ├── index.html
│   ├── package.json
│   └── vite.config.js          ← Vite config with API proxy
│
├── scripts/
│   └── simulate_alerts.py      ← Alert simulator for testing
│
├── docs/                       ← Documentation
│   ├── API.md                  ← API endpoint reference
│   ├── SETUP.md                ← Setup instructions
│   └── TEAM_GUIDE.md           ← THIS FILE
│
├── .gitignore
└── README.md
```

---

## 👥 Role Assignments & File Ownership

| Role | Works In | Files They Own |
|------|----------|----------------|
| **Backend API** | `backend/app/routes/` | `incidents.py`, `alerts.py` |
| **Database/Models** | `backend/app/models/` | `incident.py`, `database.py` |
| **Classification Engine** | `backend/app/services/` | `classification.py`, `notification.py` |
| **WebSocket/Real-time** | `backend/app/routes/` + `frontend/` | `websocket.py` + WebSocket client code |
| **Frontend Dashboard** | `frontend/src/` | All `.jsx` and `.css` files |
| **Alert Simulator** | `scripts/` | `simulate_alerts.py` |
| **Team Lead / Integrator** | Everywhere | Reviews PRs, merges, tests integration |

### ⚠️ GOLDEN RULE
> **DO NOT edit files outside your assigned folder.**
> If you need something from another folder, ASK the person who owns it.

---

## 🔀 Git Workflow (MUST FOLLOW)

### Every time you start working:
```bash
# 1. Go to dev, get latest code
git checkout dev
git pull origin dev

# 2. Go back to your branch and merge latest dev
git checkout feature/your-task-name
git merge dev
```

### When you want to save your progress:
```bash
git add .
git commit -m "Short clear message about what you did"
git push origin feature/your-task-name
```

### When your feature is ready:
1. Push your branch
2. Go to GitHub → Create **Pull Request**
3. Set **base branch = `dev`** (NOT main!)
4. Add a description of what you built
5. Wait for team lead to review and merge

### Commit Message Examples (GOOD ✅)
```
Added incident acknowledge/resolve endpoints
Fixed classification for high-CPU alerts
Styled incident cards with severity colors
Connected WebSocket to dashboard
```

### Commit Message Examples (BAD ❌)
```
update
fix
changes
asdfg
done
```

---

## ❌ STRICT RULES — READ THIS

| ❌ NEVER DO THIS | ✅ ALWAYS DO THIS |
|---|---|
| Push directly to `main` | Use feature branches |
| Push directly to `dev` | Create Pull Requests |
| Edit someone else's files | Ask them first |
| Work without pulling latest | `git pull origin dev` before starting |
| Make one giant commit at the end | Commit small, commit often |
| Install new packages without telling team | Inform in group chat first |

---

## 🔌 API Reference (For Frontend Team)

The backend serves these endpoints. Frontend team should use these:

### Base URL: `http://localhost:8000` (proxied via Vite, so just use `/api/...`)

| Action | Method | URL | Body |
|--------|--------|-----|------|
| List all incidents | GET | `/api/incidents/` | — |
| Get one incident | GET | `/api/incidents/{id}` | — |
| Create incident | POST | `/api/incidents/` | `{title, severity, ...}` |
| Acknowledge | PATCH | `/api/incidents/{id}/acknowledge` | — |
| Escalate | PATCH | `/api/incidents/{id}/escalate` | — |
| Resolve | PATCH | `/api/incidents/{id}/resolve` | — |
| Ingest alert | POST | `/api/alerts/ingest` | `{type, message, source}` |

### WebSocket: `ws://localhost:8000/ws`

Full API docs: see `docs/API.md` or open `http://localhost:8000/docs` (Swagger UI)

---

## 🗄️ Database — How It Works

### During Development (Everyone)
- Uses **SQLite** — a simple file-based database
- The file `incidents.db` is auto-created in `backend/` folder
- **No MySQL installation needed**
- The database is local to YOUR machine (not shared)
- If you mess up, just delete `incidents.db` and restart the server — it recreates itself

### For Final Demo (Team Lead Only)
- Team lead can switch to MySQL by changing `DATABASE_URL` in `.env`:
  ```
  DATABASE_URL=mysql+pymysql://root:password@localhost:3306/incident_management
  ```
- This only matters for the final demo, not during development

### Important:
- `incidents.db` is in `.gitignore` — it will NOT be pushed to GitHub
- Each person has their own separate local database
- This is fine! The code is the same, only the data is different

---

## 🧪 Testing Your Work

### Backend Team
1. Start the server: `uvicorn main:app --reload`
2. Open `http://localhost:8000/docs` (Swagger)
3. Test each endpoint using the "Try it out" button
4. Run the alert simulator: `python ../scripts/simulate_alerts.py`

### Frontend Team
1. Start backend first (port 8000)
2. Start frontend: `npm run dev` (port 5173)
3. Open `http://localhost:5173`
4. Check that incidents show up, buttons work, etc.

---

## 🆘 Common Problems & Fixes

### "Cannot connect to database"
→ Make sure your `.env` has `DATABASE_URL=sqlite:///./incidents.db`

### "npm install fails"
→ Make sure you have Node.js 18+ installed: `node --version`

### "pip install fails"
→ Make sure your virtual environment is activated: `venv\Scripts\activate`

### "Merge conflict"
→ Don't panic. Call the team lead. They will resolve it.

### "Port 8000 already in use"
→ Kill the old process or use a different port: `uvicorn main:app --reload --port 8001`

### "Frontend shows blank page"
→ Check browser console (F12) for errors. Make sure backend is running.

---

## 📞 Communication Rules

1. **Update the group chat** before starting work and after pushing
2. **Ask before editing** someone else's files
3. **Pull latest code** every 2-3 hours
4. **Report blockers immediately** — don't waste time stuck alone
5. **Small commits, frequent pushes** — don't hoard code locally

---

## ⏰ Hackathon Timeline Suggestion

| Time Block | Focus |
|------------|-------|
| Hour 0-2 | Setup + understand the scaffold |
| Hour 2-6 | Build core features (backend API, frontend UI) |
| Hour 6-8 | First integration test (connect frontend to backend) |
| Hour 8-12 | Build remaining features (WebSocket, classification, notifications) |
| Hour 12-14 | Second integration test + bug fixes |
| Hour 14-16 | Polish UI, edge cases, alert simulator |
| Hour 16-18 | Final testing + demo preparation |

---

## 🏁 Final Checklist (Before Demo)

- [ ] Backend runs without errors
- [ ] Frontend connects to backend
- [ ] Alerts can be ingested via API
- [ ] Incidents appear on dashboard in real-time
- [ ] Acknowledge/Escalate/Resolve buttons work
- [ ] At least 1 infrastructure incident + 1 application incident demo ready
- [ ] Classification shows correct severity and team assignment
- [ ] README is updated with final details

---

**Questions? Ask the team lead. Don't guess. Don't waste time.**

Good luck team! 🚀
