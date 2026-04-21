# 👥 Team Roles & Responsibilities

> Based on the **NTAC:SNS-20 Problem Statement** — Event-Driven Incident Management System

---

## 🎯 What Judges Will Evaluate (4 Deliverables)

| # | Deliverable | Weight | Description |
|---|-----------|--------|-------------|
| 1 | **Incident Management Engine** | HIGH | Backend that ingests alerts, classifies them, runs workflows, sends notifications |
| 2 | **Dashboard UI** | HIGH | Real-time web UI showing incidents, severity, status, with manual controls |
| 3 | **Simulated Alert Input** | MEDIUM | Script to generate both infrastructure AND application alerts for demo |
| 4 | **Presentation & Demo** | HIGH | Walk through 1 infra incident + 1 app incident start-to-finish |

---

## 🧩 Role Definitions (Based on Deliverables)

### ROLE 1: Backend Core — API & Workflow Engine
> **Deliverable it serves:** #1 (Incident Management Engine)

**What you build:**
- All incident CRUD API endpoints (create, read, update, delete)
- **Incident lifecycle workflow**: `NEW → ACKNOWLEDGED → ESCALATED → RESOLVED`
- Status validation (e.g., can't resolve a "new" incident without acknowledging first)
- Filtering & sorting (by severity, status, date)
- Error handling & input validation

**Files you own:**
```
backend/app/routes/incidents.py    ← Main API endpoints
backend/app/routes/alerts.py       ← Alert ingestion endpoint
backend/main.py                    ← Only if adding new routers
```

**Your branch:** `feature/backend-api`

**Hour-by-hour plan:**
| Hours | Task |
|-------|------|
| 0-2 | Setup environment, understand the scaffold, run the server |
| 2-5 | Complete all incident endpoints with proper validation |
| 5-7 | Build the alert ingestion pipeline (receive alert → classify → create incident) |
| 7-9 | Add filtering, sorting, workflow validation rules |
| 9-11 | Connect with WebSocket person to broadcast on incident changes |
| 11-14 | Test all endpoints via Swagger, fix bugs |
| 14-16 | Polish edge cases, add error messages |
| 16-18 | Final testing with full team |

**Definition of DONE:**
- [ ] POST `/api/alerts/ingest` creates incident with correct severity & team
- [ ] All lifecycle endpoints work (acknowledge, escalate, resolve)
- [ ] Status transitions are validated (can't skip steps)
- [ ] Swagger docs show all endpoints clearly

---

### ROLE 2: Classification Engine & Notifications
> **Deliverable it serves:** #1 (Incident Management Engine)

**What you build:**
- **Classification logic**: Determine severity (critical/high/medium/low) based on alert type
- **Team routing**: Infrastructure alerts → DevOps Team, Application alerts → App Team
- **Notification system**: Send alerts via at least ONE channel (email OR Slack webhook OR SMS)
- **Escalation logic**: If a critical incident is not acknowledged within X minutes → auto-escalate

**Files you own:**
```
backend/app/services/classification.py   ← Classification rules
backend/app/services/notification.py     ← Notification sending
backend/app/models/incident.py           ← If you need to add fields
backend/app/database.py                  ← If you need to change DB config
```

**Your branch:** `feature/classification-notifications`

**Hour-by-hour plan:**
| Hours | Task |
|-------|------|
| 0-2 | Setup environment, understand classification.py scaffold |
| 2-5 | Build comprehensive classification rules (see rules table below) |
| 5-8 | Implement at least 1 notification channel (Slack webhook is easiest) |
| 8-10 | Add escalation timer logic (background task or check on API call) |
| 10-13 | Test classification with different alert types |
| 13-15 | Integration test with backend API person |
| 15-18 | Polish, edge cases, demo prep |

**Classification Rules to Implement:**

| Source | Alert Contains | Severity | Assign To |
|--------|---------------|----------|-----------|
| Infrastructure | "down", "outage", "failure", "crash", "unreachable" | `critical` | DevOps Team |
| Infrastructure | "high cpu", "high memory", "disk full", "latency" | `high` | DevOps Team |
| Infrastructure | anything else | `medium` | DevOps Team |
| Application | "unresponsive", "crash", "data loss" | `critical` | Application Team |
| Application | "error rate", "timeout", "exception" | `high` | Application Team |
| Application | anything else | `low` | Application Team |

**Notification Options (pick ONE to implement):**
- **Slack Webhook** (EASIEST) — just POST JSON to a webhook URL
- **Email via SMTP** — use Python's `smtplib` with Gmail
- **SMS via Twilio** — needs Twilio account (free trial available)
- **Console/Log** (MINIMUM) — structured log output showing notifications

**Definition of DONE:**
- [ ] Classification correctly assigns severity for all alert types
- [ ] Infrastructure vs Application alerts route to different teams
- [ ] At least 1 notification channel works (even if just logging)
- [ ] Critical infrastructure alerts get different treatment than low app alerts

---

### ROLE 3: Real-Time WebSocket & Integration
> **Deliverable it serves:** #1 + #2 (Backend + Dashboard connection)

**What you build:**
- **WebSocket server**: Broadcast incident changes to all connected dashboard clients
- **WebSocket client**: Frontend code that listens for real-time updates
- **Auto-refresh**: Dashboard updates WITHOUT page reload when incidents change
- **Live connection indicator**: Show if dashboard is connected to backend

**Files you own:**
```
backend/app/routes/websocket.py          ← WebSocket server
frontend/src/hooks/useWebSocket.js       ← NEW: Custom React hook for WS (create this)
```

**Files you COORDINATE with (don't own):**
```
backend/app/routes/incidents.py          ← Ask backend person to call broadcast()
backend/app/routes/alerts.py             ← Ask backend person to call broadcast()
frontend/src/pages/Dashboard.jsx         ← Ask frontend person to use your hook
```

**Your branch:** `feature/websocket-realtime`

**Hour-by-hour plan:**
| Hours | Task |
|-------|------|
| 0-2 | Setup, understand websocket.py scaffold |
| 2-5 | Make WebSocket broadcast work: when incident created → push to all clients |
| 5-8 | Build React custom hook `useWebSocket.js` for frontend |
| 8-10 | Coordinate with frontend person to integrate the hook into Dashboard |
| 10-12 | Coordinate with backend person to add broadcast calls in routes |
| 12-15 | Test: create incident → dashboard updates instantly |
| 15-18 | Polish, reconnection logic, connection indicator |

**WebSocket Message Format (agree with frontend):**
```json
{
  "type": "incident_created",
  "data": { "id": 1, "title": "...", "severity": "critical", ... }
}
```
```json
{
  "type": "incident_updated",
  "data": { "id": 1, "status": "acknowledged", ... }
}
```

**Definition of DONE:**
- [ ] Dashboard updates in real-time when alert is ingested (no page refresh)
- [ ] Dashboard updates when incident status changes
- [ ] WebSocket reconnects if connection drops

---

### ROLE 4: Frontend Dashboard
> **Deliverable it serves:** #2 (User Interface / Dashboard)

**What you build:**
- **Incident list view**: Cards showing all incidents with severity badges
- **Status filter tabs**: Filter by new / acknowledged / escalated / resolved
- **Manual controls**: Acknowledge, Escalate, Resolve buttons that call the API
- **Stats overview**: Counts of total, critical, open, resolved incidents
- **Visual design**: Dark theme, color-coded severity, responsive layout
- **Incident detail view** (bonus): Click to see full incident details

**Files you own:**
```
frontend/src/pages/Dashboard.jsx + .css
frontend/src/components/IncidentCard.jsx + .css
frontend/src/components/StatsBar.jsx + .css
frontend/src/App.jsx
frontend/src/index.css
frontend/index.html
```

**Your branch:** `feature/frontend-dashboard`

**Hour-by-hour plan:**
| Hours | Task |
|-------|------|
| 0-2 | Setup, run frontend, understand the scaffold components |
| 2-5 | Build the full dashboard layout (header, stats, filters, grid) |
| 5-8 | Style incident cards with severity colors, badges, animations |
| 8-10 | Add action buttons (acknowledge, escalate, resolve) with API calls |
| 10-12 | Coordinate with WebSocket person to add real-time updates |
| 12-14 | Add incident detail view (modal or expandable card) |
| 14-16 | Polish: hover effects, animations, loading states, empty states |
| 16-18 | Final UI cleanup for demo |

**Key Requirement from Problem Statement:**
> The dashboard must show: severity, status, assigned team, timestamp.
> It must allow: acknowledge, escalate, resolve actions.

**Definition of DONE:**
- [ ] All incidents display with severity, status, team, timestamp
- [ ] Action buttons work (acknowledge, escalate, resolve)
- [ ] Filter tabs filter correctly
- [ ] Stats bar shows accurate counts
- [ ] UI looks polished and professional for demo

---

### ROLE 5: Alert Simulator & Demo Prep
> **Deliverable it serves:** #3 + #4 (Simulated Alerts + Presentation)

**What you build:**
- **Alert simulator script**: Generates realistic infrastructure + application alerts
- **Demo scenarios**: Pre-planned incident flows for the presentation
- **README update**: Final documentation for submission
- **Presentation slides** (optional): If the hackathon requires slides

**Files you own:**
```
scripts/simulate_alerts.py     ← Alert generator
docs/                          ← Documentation
README.md                      ← Final README
```

**Your branch:** `feature/alert-simulator`

**Hour-by-hour plan:**
| Hours | Task |
|-------|------|
| 0-2 | Setup, understand the system flow |
| 2-5 | Build comprehensive alert simulator with realistic scenarios |
| 5-8 | Add continuous mode (alerts keep coming every few seconds) |
| 8-12 | Help test other people's features using the simulator |
| 12-14 | Prepare demo scenarios (see below) |
| 14-16 | Update README with final architecture, screenshots |
| 16-18 | Practice the demo presentation |

**Demo Scenarios to Prepare:**

**Scenario 1 — Infrastructure (Critical):**
```
Alert: "Production server web-01 is unreachable"
→ System classifies: CRITICAL severity
→ Assigns: DevOps Team
→ Notification: Sent to on-call engineer
→ Dashboard: Shows red critical card
→ Action: Team lead acknowledges → resolves
```

**Scenario 2 — Application (Low/Medium):**
```
Alert: "Error rate spike on /api/orders endpoint"
→ System classifies: HIGH severity
→ Assigns: Application Team
→ Notification: Email to app team
→ Dashboard: Shows orange high card
→ Action: Assess → escalate if needed → resolve
```

**Definition of DONE:**
- [ ] Simulator generates at least 10 different alert types
- [ ] Covers both infrastructure AND application incidents
- [ ] Continuous mode available for live demo
- [ ] Demo script prepared for 2 scenarios
- [ ] README is complete and professional

---

### ROLE 6: Team Lead / System Integrator (YOUR ROLE)
> **Deliverable it serves:** ALL — you are the glue

**What you do:**
- Review and merge all Pull Requests
- Test integration every 3-4 hours
- Fix merge conflicts
- Coordinate between backend/frontend/WebSocket people
- Switch to MySQL for final demo
- Run the final demo presentation
- Make final README + submission

**Your branch:** You work directly on `dev` for integration fixes only

**Hour-by-hour plan:**
| Hours | Task |
|-------|------|
| 0-2 | Ensure everyone has cloned, set up, and is on their feature branch |
| 2-4 | Check in with each person, answer questions |
| 4-6 | **MERGE ROUND 1**: Review PRs, merge to dev, test backend+frontend connection |
| 6-8 | Fix any integration bugs from round 1 |
| 8-10 | **MERGE ROUND 2**: Merge WebSocket + classification PRs, test real-time |
| 10-12 | Fix integration bugs from round 2 |
| 12-14 | **MERGE ROUND 3**: Full end-to-end test with all features |
| 14-16 | Bug fixes, polish, help whoever is behind |
| 16-17 | **FINAL MERGE**: `dev → main`, switch to MySQL, clean test |
| 17-18 | Practice demo, final submission |

**Integration Test Checklist (run every merge round):**
- [ ] `uvicorn main:app --reload` starts without errors
- [ ] `npm run dev` shows dashboard
- [ ] Alert simulator creates incidents
- [ ] Incidents appear on dashboard
- [ ] Classification assigns correct severity/team
- [ ] Action buttons work
- [ ] (After WebSocket merge) Dashboard updates in real-time

---

## 🔗 How Roles Connect (Data Flow)

```
ROLE 5 (Simulator)
    ↓ sends alerts
ROLE 1 (Backend API) ←→ ROLE 2 (Classification)
    ↓ saves to DB
    ↓ broadcasts via
ROLE 3 (WebSocket)
    ↓ pushes to
ROLE 4 (Frontend Dashboard)
    ↓ user clicks buttons
ROLE 1 (Backend API) ← processes actions
    
ROLE 6 (Team Lead) ← integrates everything
```

---

## 📊 Role Assignment Template

Copy this and fill in team member names:

| Role # | Role Name | Person | Branch Name |
|--------|-----------|--------|-------------|
| 1 | Backend Core (API + Workflow) | __________ | `feature/backend-api` |
| 2 | Classification + Notifications | __________ | `feature/classification-notifications` |
| 3 | WebSocket + Real-time | __________ | `feature/websocket-realtime` |
| 4 | Frontend Dashboard | __________ | `feature/frontend-dashboard` |
| 5 | Alert Simulator + Demo | __________ | `feature/alert-simulator` |
| 6 | Team Lead / Integrator | __________ (YOU) | works on `dev` |

### If you have fewer than 6 people, combine roles:

**5 people:**
- Combine Role 3 (WebSocket) into Role 1 (Backend) → same person does API + WebSocket

**4 people:**
- Combine Role 3 into Role 1 (Backend does API + WebSocket)
- Combine Role 5 into Role 6 (Team lead also does simulator + demo prep)

**3 people:**
- Person 1: Role 1 + 2 + 3 (entire backend)
- Person 2: Role 4 (entire frontend)
- Person 3: Role 5 + 6 (simulator + team lead)

---

## ⚠️ Critical Dependencies (Don't Miss These)

| If you are... | You NEED from... | By hour... |
|---------------|-------------------|-----------|
| Frontend (Role 4) | Backend API endpoints working (Role 1) | Hour 4-5 |
| Frontend (Role 4) | WebSocket hook (Role 3) | Hour 10 |
| Backend API (Role 1) | Classification function (Role 2) | Hour 4-5 |
| WebSocket (Role 3) | Backend to call broadcast() (Role 1) | Hour 8-10 |
| Simulator (Role 5) | Alert ingestion API working (Role 1) | Hour 4-5 |
| Team Lead (Role 6) | Everyone's first PR | Hour 5-6 |

---

**Remember: The demo is what gets judged. Everything should work for the demo.**

Build → Test → Integrate → Demo 🚀
