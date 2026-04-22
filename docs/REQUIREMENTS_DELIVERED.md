# 📑 Project Requirements & Final Scope (Delivered)

This document outlines the initial functional requirements for the **Event-Driven Incident Management System** and documents the final scope of the project as delivered for the 24-hour NT Hackathon.

## 🎯 Primary Requirements (Met)

| Requirement | Description | Status |
| :--- | :--- | :--- |
| **Alert Ingestion** | System can intake raw JSON payloads representing system failures from external sources. | ✅ COMPLETED |
| **Real-time Dashboard** | A live web interface displaying incident state changes instantly without page refreshes. | ✅ COMPLETED |
| **Status Workflow** | Support for `NEW`, `ACKNOWLEDGED`, `ESCALATED`, and `RESOLVED` transitions. | ✅ COMPLETED |
| **Team Routing** | Automatic assignment to Infrastructure, Application, Platform, or Security teams. | ✅ COMPLETED |
| **Historical Logs** | Audit trail for every action taken on an incident (timestamped). | ✅ COMPLETED |
| **Analytical Reports** | Data visualization for severity distribution and team resolution performance. | ✅ COMPLETED |

---

## 🚀 Advanced "Value-Add" Features (Unique Innovations)

Beyond the basic requirements, our team implemented several advanced features to make the system production-ready and technically "luxurious":

### 1. 🧠 AI-Powered "Brain" (Gemini 2.5 Flash)
*   **Contextual Understanding:** We replaced basic keyword matching with a **Google Gemini-powered classification engine**. It understands intent (e.g., *"Database is slow"* vs *"Database is down"*) and adjusts severity scores dynamically.
*   **Automated Summaries:** The AI generates human-readable incident descriptions for every incoming alert.

### 2. ⚖️ Intelligent Workload balancing
*   **Burnout Prevention:** Implemented a `MAX_ACTIVE_INCIDENTS = 3` cap. The system will never overwhelm a single engineer if others are available.
*   **Normalized Routing:** New incidents are automatically routed to the member with the absolute lowest current active load.

### 3. ⏱️ 3-Strike Escalation Failsafe
*   **Live SLA Monitoring:** A background daemon monitors incidents. If not acknowledged within **2 minutes**, the incident is unassigned and rerouted.
*   **Failsafe Auto-Ack:** On the 3rd assignment failure, the system forcefully assigns the ticket and auto-acknowledges it to ensure high-priority visibility.

### 4. 💎 "Technical Luxury" UI/UX
*   **Visual Priority:** Implemented a **"Breathing Glow"** effect on new/open cards to immediately draw attention to unhandled disasters.
*   **Dynamic Trace:** A scrollable Activity Trail in the sidebar that updates in real-time as background automations or humans take action.

---

## 🛠️ Technical Compliance

*   **Frontend:** React 18 (Vite) with pure Vanilla CSS for performance.
*   **Backend:** FastAPI (Python 3.9+) with asynchronous background workers.
*   **Architecture:** Event-Driven via WebSockets and Webhooks.
*   **Database:** SQLite (SQLAlchemy ORM) with a migration path to MySQL/Postgres.

---
**Team Batch-06 | 24-Hour NT Hackathon**
