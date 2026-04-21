# 👥 Team Roles & Task Assignments

> **NTAC:SNS-20 — Event-Driven Incident Management System**
> 5-member team | 18-hour hackathon

---

## 🎯 What Judges Will Evaluate (4 Deliverables)

| # | Deliverable | Who Owns It |
|---|-------------|-------------|
| 1 | **Incident Management Engine** (Backend + DB + Classification) | Anuritha + Shivani B |
| 2 | **Dashboard UI** (Real-time web interface) | Sakshi |
| 3 | **Simulated Alert Input** (Test script) | 5th Member + Lead |
| 4 | **Presentation & Demo** (Walk through infra + app incident) | Lead (You) |

---

## 👨‍💻 ROLE 1: Lead — System Architect + Integrator (YOU)

### What you do:
- Define and finalize all API contracts
- Review & merge Pull Requests on GitHub
- Connect frontend ↔ backend ↔ WebSocket
- Test integration every 3-4 hours
- Fix merge conflicts and integration bugs
- Help whoever is stuck or behind schedule
- Prepare and deliver the final demo
- Switch to MySQL for final demo

### Files you may touch:
```
backend/main.py              ← If adding new routers
backend/app/routes/           ← For integration fixes
docs/                         ← Documentation
scripts/simulate_alerts.py    ← If 5th member needs help
```

### Your branch: Work directly on `dev` for integration fixes

### Hour-by-hour:
| Hours | Task |
|-------|------|
| 0-2 | Ensure everyone cloned, set up, and is on their feature branch |
| 2-4 | Help Anuritha with API setup, help Sakshi with frontend setup |
| 4-6 | **MERGE ROUND 1**: Merge backend + DB PRs → test API via Swagger |
| 6-8 | Help connect frontend to backend API, fix any issues |
| 8-10 | **MERGE ROUND 2**: Merge frontend + WebSocket PRs → test real-time |
| 10-12 | Integration bugfixes, help whoever is behind |
| 12-14 | **MERGE ROUND 3**: Full end-to-end test |
| 14-16 | Polish, help with alert simulator, update README |
| 16-17 | **FINAL MERGE**: `dev → main`, switch to MySQL, clean test |
| 17-18 | Practice and deliver demo |

### Integration Test Checklist (run every merge round):
- [ ] `uvicorn main:app --reload` starts without errors
- [ ] `npm run dev` shows dashboard
- [ ] Alert simulator creates incidents with correct classification
- [ ] Incidents appear on dashboard with severity colors
- [ ] Acknowledge / Escalate / Resolve buttons work
- [ ] (After WebSocket) Dashboard updates in real-time

---

## 👩‍💻 ROLE 2: Anuritha — Backend Core (APIs + Workflow)

### What you build:
- All FastAPI endpoints for incident management
- Alert ingestion pipeline (receive alert → classify → create incident)
- Incident lifecycle workflow: `NEW → ACKNOWLEDGED → ESCALATED → RESOLVED`
- Status transition validation
- Proper error handling, HTTP status codes

### Files you own:
```
backend/app/routes/incidents.py     ← All incident CRUD endpoints
backend/app/routes/alerts.py        ← Alert ingestion endpoint
backend/main.py                     ← If adding new routers
backend/requirements.txt            ← If adding new Python packages
```

### Your branch: `feature/backend-api`

### APIs to build:

| Method | Endpoint | What it does |
|--------|----------|-------------|
| POST | `/api/alerts/ingest` | Receive alert → classify → create incident |
| GET | `/api/incidents/` | List all incidents (newest first) |
| GET | `/api/incidents/{id}` | Get single incident details |
| PATCH | `/api/incidents/{id}/acknowledge` | Status: new → acknowledged |
| PATCH | `/api/incidents/{id}/escalate` | Status: → escalated |
| PATCH | `/api/incidents/{id}/resolve` | Status: → resolved |
| DELETE | `/api/incidents/{id}` | Delete an incident |

### Hour-by-hour:
| Hours | Task |
|-------|------|
| 0-2 | Setup: clone repo, create venv, install deps, run server |
| 2-4 | Build `/api/alerts/ingest` endpoint (calls Shivani's classification) |
| 4-6 | Build all incident CRUD endpoints with validation |
| 6-8 | Add lifecycle workflow rules (status transition validation) |
| 8-10 | Work with Lead to add WebSocket broadcast calls in routes |
| 10-12 | Test all endpoints via Swagger UI |
| 12-14 | Create PR → Lead merges → fix any integration issues |
| 14-16 | Add filtering (by severity, status), sorting, edge cases |
| 16-18 | Final testing with full team |

### Definition of DONE:
- [ ] All 7 endpoints work and return correct data
- [ ] Alert ingestion calls classification and creates incident correctly
- [ ] Status transitions are validated (can't resolve without acknowledging)
- [ ] Swagger UI shows all endpoints with clear documentation

### ⚠️ You depend on:
- **Shivani's classification function** (needed by hour 4) — if she's not done yet, use a simple placeholder:
  ```python
  # Temporary until Shivani's code is ready
  severity = "critical" if "server" in alert_type else "low"
  assigned_to = "DevOps Team" if source == "infrastructure" else "App Team"
  ```

---

## 👩‍💻 ROLE 3: Shivani B — Database + Classification Logic

### What you build:
- MySQL/SQLite database schema (model is already scaffolded)
- **Classification engine**: Determine severity based on alert keywords
- **Team routing**: Infrastructure → DevOps, Application → App Team
- **Assignment logic**: Smart routing based on alert content

### Files you own:
```
backend/app/models/incident.py           ← Database model (add fields if needed)
backend/app/database.py                  ← Database config
backend/app/services/classification.py   ← Classification rules (THIS IS YOUR MAIN FILE)
backend/app/services/notification.py     ← Notification stubs
```

### Your branch: `feature/db-classification`

### Classification Rules to implement:

```python
# Infrastructure alerts
if source == "infrastructure":
    if any keyword in ["down", "outage", "failure", "crash", "unreachable"]:
        severity = "critical"
    elif any keyword in ["high cpu", "high memory", "disk full", "latency"]:
        severity = "high"
    else:
        severity = "medium"
    assigned_to = "DevOps Team"

# Application alerts
elif source == "application":
    if any keyword in ["unresponsive", "crash", "data loss"]:
        severity = "critical"
    elif any keyword in ["error rate", "timeout", "exception"]:
        severity = "high"
    else:
        severity = "low"
    assigned_to = "Application Team"
```

### Hour-by-hour:
| Hours | Task |
|-------|------|
| 0-2 | Setup: clone repo, create venv, understand `incident.py` model |
| 2-4 | Build complete classification rules in `classification.py` |
| 4-6 | Test classification with different alert types (write test cases) |
| 6-8 | Add any extra model fields if needed (e.g., `escalation_level`) |
| 8-10 | Build notification service (at minimum: structured logging) |
| 10-12 | Create PR → Lead merges |
| 12-14 | Help Anuritha test the full pipeline (alert → classify → incident) |
| 14-16 | Add more classification rules, edge cases |
| 16-18 | Final testing |

### Definition of DONE:
- [ ] `classify_alert()` returns correct severity for all alert types
- [ ] Infrastructure alerts → DevOps Team, Application alerts → App Team
- [ ] At least 6+ different alert types are classified correctly
- [ ] Model has all required fields (id, title, severity, status, assigned_to, created_at, updated_at)

### ⚠️ Anuritha depends on you:
She needs your `classify_alert()` function by **hour 4**. Push early!

---

## 👩‍💻 ROLE 4: Sakshi — Frontend Dashboard (React)

### What you build:
- Full incident dashboard with dark theme UI
- Incident cards with severity badges (colored: red/orange/yellow/green)
- Status filter tabs (All / New / Acknowledged / Escalated / Resolved)
- Action buttons (Acknowledge, Escalate, Resolve) that call the API
- Stats bar (total, critical, open, resolved counts)
- Real-time updates via WebSocket (coordinate with 5th member)

### Files you own:
```
frontend/src/pages/Dashboard.jsx + .css       ← Main dashboard page
frontend/src/components/IncidentCard.jsx + .css ← Incident card component
frontend/src/components/StatsBar.jsx + .css     ← Stats bar component
frontend/src/App.jsx                            ← Router (add new pages if needed)
frontend/src/index.css                          ← Global styles / design tokens
frontend/index.html                             ← HTML entry point
frontend/src/main.jsx                           ← React entry point
```

### Your branch: `feature/frontend-dashboard`

### What the dashboard MUST show (from problem statement):
- Severity (with color coding)
- Status (new / acknowledged / escalated / resolved)
- Assigned team
- Timestamp
- Action buttons: Acknowledge, Escalate, Resolve

### Hour-by-hour:
| Hours | Task |
|-------|------|
| 0-2 | Setup: clone, `npm install`, `npm run dev`, understand scaffold |
| 2-4 | Build the full dashboard layout (header, stats bar, card grid) |
| 4-6 | Style incident cards: severity badges, status colors, metadata |
| 6-8 | Connect to backend API: fetch incidents, display in cards |
| 8-10 | Add action buttons: Acknowledge, Escalate, Resolve (PATCH calls) |
| 10-12 | Add filter tabs, sorting, loading states |
| 12-14 | Coordinate with 5th member to add WebSocket real-time updates |
| 14-16 | Polish: animations, hover effects, responsive layout, empty states |
| 16-18 | Final UI cleanup for demo |

### API calls you'll make:
```javascript
// Fetch all incidents
fetch('/api/incidents/')

// Acknowledge an incident
fetch('/api/incidents/5/acknowledge', { method: 'PATCH' })

// Escalate an incident
fetch('/api/incidents/5/escalate', { method: 'PATCH' })

// Resolve an incident
fetch('/api/incidents/5/resolve', { method: 'PATCH' })
```

> Note: Vite proxies `/api/*` to `localhost:8000` — so you just write `/api/...` in your code.

### Definition of DONE:
- [ ] Dashboard displays all incidents in a card grid
- [ ] Each card shows: title, severity badge, status badge, team, timestamp
- [ ] Filter tabs work (All / New / Acknowledged / Escalated / Resolved)
- [ ] Action buttons call correct API endpoints
- [ ] Stats bar shows accurate counts
- [ ] Dark theme with severity color coding looks polished

### ⚠️ You depend on:
- **Backend API working** (Anuritha) — by hour 6. Until then, use mock data:
  ```javascript
  const mockIncidents = [
    { id: 1, title: "Server down", severity: "critical", status: "new", assigned_to: "DevOps Team", source: "infrastructure", created_at: new Date().toISOString() },
    { id: 2, title: "App error", severity: "low", status: "new", assigned_to: "Application Team", source: "application", created_at: new Date().toISOString() },
  ];
  ```

---

## 👨‍💻 ROLE 5: 5th Member — WebSocket + Alert Simulator + Notifications

### What you build:
- **WebSocket server**: Broadcast incident changes to dashboard in real-time
- **WebSocket client**: React hook for frontend to receive real-time updates
- **Alert simulator**: Script that generates realistic test alerts
- **Notifications**: At least log-based notification when incidents are created

### Files you own:
```
backend/app/routes/websocket.py    ← WebSocket server (broadcast manager)
backend/app/services/notification.py ← Notification service
scripts/simulate_alerts.py          ← Alert simulator script
frontend/src/hooks/               ← NEW folder: create useWebSocket.js hook
```

### Your branch: `feature/realtime-simulator`

### Hour-by-hour:
| Hours | Task |
|-------|------|
| 0-2 | Setup: clone, install, understand websocket.py scaffold |
| 2-4 | Build comprehensive alert simulator with 10+ alert types |
| 4-6 | Add continuous mode (send alerts every few seconds for live demo) |
| 6-8 | Wire WebSocket: broadcast when incident is created/updated |
| 8-10 | Create React `useWebSocket.js` hook for frontend |
| 10-12 | Coordinate with Sakshi to integrate WebSocket into Dashboard |
| 12-14 | Build notification service (Slack webhook OR structured logging) |
| 14-16 | Test full real-time flow: simulator → backend → WebSocket → dashboard |
| 16-18 | Final testing, help with demo prep |

### WebSocket broadcast — ask Anuritha to add this in her routes:
```python
# In incidents.py and alerts.py, after creating/updating incident:
from app.routes.websocket import manager
await manager.broadcast({
    "type": "incident_created",  # or "incident_updated"
    "data": incident.to_dict()
})
```

### React hook to create (`frontend/src/hooks/useWebSocket.js`):
```javascript
import { useEffect, useRef, useState } from 'react';

export function useWebSocket(url) {
  const [lastMessage, setLastMessage] = useState(null);
  const ws = useRef(null);

  useEffect(() => {
    ws.current = new WebSocket(url);
    ws.current.onmessage = (event) => {
      setLastMessage(JSON.parse(event.data));
    };
    return () => ws.current?.close();
  }, [url]);

  return { lastMessage };
}
```

### Definition of DONE:
- [ ] Alert simulator sends 10+ different alert types
- [ ] Continuous mode works for live demo
- [ ] WebSocket broadcasts when incidents are created/updated
- [ ] Dashboard updates in real-time (no page refresh needed)
- [ ] At least one notification channel works (even if just logging)

---

## 🔗 Dependency Map — Who Needs Who & When

```
Hour 0-4:  EVERYONE works independently (setup + core logic)

Hour 4:    Shivani → Anuritha (classification function needed)
Hour 6:    Anuritha → Sakshi (API endpoints needed for frontend)
Hour 6:    Anuritha → 5th Member (API needed for simulator testing)
Hour 8:    5th Member → Anuritha (add broadcast calls in routes)
Hour 10:   5th Member → Sakshi (WebSocket hook for dashboard)
Hour 12:   EVERYONE → Lead (all PRs should be in for merge round 3)
Hour 16:   Lead → EVERYONE (final merge to main)
```

```
Shivani (classification)
    ↓ provides classify_alert()
Anuritha (backend API)
    ↓ provides endpoints
    ↓ calls broadcast()
5th Member (WebSocket + simulator)
    ↓ pushes real-time updates
Sakshi (frontend dashboard)
    ↓ shows everything to user

Lead (YOU) ← integrates all pieces
```

---

## ⏰ Execution Timeline (Synchronized)

| Hours | Anuritha (Backend) | Shivani (DB+Logic) | Sakshi (Frontend) | 5th Member (RT+Sim) | Lead (You) |
|-------|--------------------|--------------------|-------------------|---------------------|------------|
| 0-2 | Setup + understand | Setup + understand | Setup + understand | Setup + understand | Help everyone setup |
| 2-4 | Alert ingestion API | Classification rules | Dashboard layout | Alert simulator | Check-ins |
| 4-6 | CRUD endpoints | Test classification | Style cards + badges | Continuous mode | **MERGE ROUND 1** |
| 6-8 | Lifecycle validation | Notification stubs | Connect to API | Wire WebSocket | Integration fixes |
| 8-10 | Add broadcast calls | Help Anuritha test | Action buttons | React WS hook | **MERGE ROUND 2** |
| 10-12 | Edge cases, filters | Polish classification | WebSocket integration | Test real-time flow | Integration fixes |
| 12-14 | Final PR + fixes | Final PR | Filter tabs, polish | Notification service | **MERGE ROUND 3** |
| 14-16 | Bug fixes | Help test | Animations, responsive | Demo scenarios | Polish, help |
| 16-17 | Final test | Final test | Final test | Final test | **FINAL MERGE** |
| 17-18 | Demo support | Demo support | Demo support | Demo support | **RUN DEMO** |

---

## 🎬 Demo Script (Lead prepares this)

### Scenario 1 — Infrastructure Incident (Critical):
1. Show empty dashboard
2. Run simulator → alert: "Production server web-01 is unreachable"
3. System classifies: **CRITICAL** severity
4. Assigns to: **DevOps Team**
5. Notification logged: "On-call engineer notified"
6. Dashboard shows red critical card in real-time
7. Click **Acknowledge** → status changes to "acknowledged"
8. Click **Resolve** → status changes to "resolved"
9. Stats bar updates

### Scenario 2 — Application Incident (Lower Priority):
1. Alert: "Error rate spike on /api/orders endpoint"
2. System classifies: **HIGH** severity
3. Assigns to: **Application Team**
4. Notification: "App team notified via email"
5. Dashboard shows orange card
6. Show it takes different path than infrastructure
7. Click **Escalate** → status changes
8. Click **Resolve** → done

### Key points to highlight for judges:
- Different classification paths (infra vs app)
- Automatic team assignment
- Incident lifecycle workflow (NEW → ACK → ESCALATE → RESOLVE)
- Real-time dashboard updates
- Notification system

---

**Share this doc with your team. Everyone reads their role section and starts coding.**

Good luck! 🚀
