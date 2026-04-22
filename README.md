# 🚨 Event-Driven Incident Management System

## 📌 Overview

This project is a simplified **Event-Driven Incident Management System** built to simulate how modern DevOps teams detect, classify, and resolve system incidents in real-time.

The system processes incoming alerts, utilizes Google Gemini AI to classify them into structured incidents, rigorously balances active assignment workloads, and auto-escalates critical alerts when engineers fail to acknowledge them.

---

## 🎯 Problem We Are Solving

In real-world systems, failures such as server crashes or application errors require quick detection and response.

Our solution demonstrates:

* How alerts can be automatically processed
* How incidents can be prioritized and routed
* How teams can monitor and resolve issues efficiently

---

## ⚙️ Core Features

### 🔹 AI-Powered Alert Ingestion

* Simulated alerts are instantly processed via Google Gemini 2.5 Flash to automatically detect severity, classify infrastructure issues, and write human-readable incident summaries.

### 🔹 Classification & Routing

* Categorizes incidents into severity levels:

  * Critical
  * Low
* Automatically balances workloads and assigns incidents to the least busy engineer across 4 primary teams:

  * Infrastructure Team
  * Application Team
  * Platform Team
  * Security Team

### 🔹 Incident Lifecycle

Each incident progresses through:

```text
NEW → ACKNOWLEDGED → RESOLVED
```

### 🔹 Auto-Escalation & 3-Strike Failsafe

* If a critical incident goes unacknowledged for 2 minutes, it is auto-escalated and rerouted.
* If it fails 3 assignments, a hard failsafe forcefully assigns it to the least busy engineer and auto-acknowledges it.

### 🔹 Dashboard (UI)

* Displays all incidents in real-time
* Shows:

  * Severity
  * Status
  * Assigned team
  * Timestamp

### 🔹 Manual Controls

* Acknowledge incidents
* Resolve incidents

### 🔹 Real-Time Updates

* Live updates using WebSockets

---

## 🏗️ System Architecture

```text
[Alert Generator]
        ↓
[FastAPI Backend]
        ↓
[Gemini AI Classification]
        ↓
[SQLite Database]
        ↓
[WebSocket Layer]
        ↓
[React Dashboard]
```

---

## 🧰 Tech Stack

| Layer       | Technology                   |
| ----------- | ---------------------------- |
| **Backend** | FastAPI, Python Background Threads |
| **Frontend**| React 18 + Vanilla CSS       |
| **Database**| SQLite via SQLAlchemy ORM    |
| **AI Block**| Google Gemini 2.5 Flash SDK  |
| **Realtime**| WebSockets                   |

---

## 🔁 Workflow

1. Alert is generated (simulated)
2. System classifies severity
3. Incident is created in database
4. Assigned to appropriate team
5. Dashboard updates in real-time
6. User performs actions (acknowledge/resolve)

---

## 🧪 Demo Scenarios

### 🔴 Critical Incident

* Example: Server Down
* Severity: Critical
* Assigned to: DevOps Team

### 🟡 Low Severity Incident

* Example: Application Error
* Severity: Low
* Assigned to: Application Team

---

## 📊 Data Model (Simplified)

**Incidents Table**

* id
* title
* severity
* status
* assigned_to
* created_at
* updated_at

---

## 🚀 How to Run

### Backend

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate   # (Windows)
# source venv/bin/activate # (Mac/Linux)

pip install -r requirements.txt
```

Create a `.env` file in the `backend/` directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Start the Backend Server:
```bash
uvicorn main:app --reload --port 8000
```

### 2. Frontend Setup
Open a second terminal and navigate to the frontend directory:
```bash
cd frontend
npm install
npm run dev
```

### 3. Simulate Ingestion (Live Demo)
Open a third terminal and inject the mock alert payloads to watch the AI Engine classifying workloads in real-time:
```bash
python scripts/simulate_alerts.py
```

---

## 👥 Team Contribution

* Backend Development (API + Logic)
* Database Design
* Frontend Dashboard
* Real-time Integration
* Testing & Demo Preparation

---

## 💡 Design Approach

We focused on:

* Simplicity and clarity
* Complete working flow
* Real-time visibility
* Clean and understandable architecture

---

## 🔮 Future Enhancements

*   **Notification Integrations:** Connect the `notification.py` stub pipelines to real-world Twilio (SMS), SendGrid (Email), or Slack Webhooks for true out-of-band alerts.
*   **PostgreSQL Migration:** Transition from the local lightweight SQLite layer to a robust distributed Postgres database.
*   **Docker Containerization:** Wrap both the frontend and backend architectures into multi-container Docker deployments for 1-click cloud launching.
*   **Custom Alert Rules:** Allow team managers to define custom keyword override boundaries without adjusting Python `_rule_based_classify` logic.

---
*Built with ❤️ by Batch-06 during an 24-hour  NT Hackathon Sprint.*
