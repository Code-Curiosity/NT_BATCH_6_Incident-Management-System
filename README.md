# 🚨 Event-Driven Incident Management System

## 📌 Overview

This project is a simplified **Event-Driven Incident Management System** built to simulate how modern DevOps teams detect, classify, and resolve system incidents in real-time.

The system processes incoming alerts, converts them into structured incidents, assigns them to relevant teams, and tracks their lifecycle through a live dashboard.

---

## 🎯 Problem We Are Solving

In real-world systems, failures such as server crashes or application errors require quick detection and response.

Our solution demonstrates:

* How alerts can be automatically processed
* How incidents can be prioritized and routed
* How teams can monitor and resolve issues efficiently

---

## ⚙️ Core Features

### 🔹 Alert Ingestion

* Simulated alerts (e.g., server down, high CPU usage, app errors)

### 🔹 Classification & Routing

* Categorizes incidents into severity levels:

  * Critical
  * Low
* Automatically assigns incidents to:

  * DevOps Team (infrastructure issues)
  * Application Team (app-level issues)

### 🔹 Incident Lifecycle

Each incident progresses through:

```text
NEW → ACKNOWLEDGED → RESOLVED
```

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
[Classification Engine]
        ↓
[MySQL Database]
        ↓
[WebSocket Layer]
        ↓
[React Dashboard]
```

---

## 🧰 Tech Stack

| Layer    | Technology           |
| -------- | -------------------- |
| Backend  | FastAPI (Python)     |
| Frontend | React + Tailwind CSS |
| Database | MySQL                |
| Realtime | WebSockets           |

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
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
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

* SLA tracking and alerts
* Incident analytics (MTTR, trends)
* Notification integration (Email/SMS/Slack)
* Role-based access control

---

## 🏁 Conclusion

This system demonstrates how an event-driven approach can improve incident response efficiency, reduce downtime, and provide better operational visibility in DevOps environments.
