# API Documentation

## Base URL
```
http://localhost:8000
```

## Endpoints

### Health Check
- `GET /` → `{ "status": "running" }`

### Incidents
| Method  | Endpoint                             | Description              |
|---------|--------------------------------------|--------------------------|
| GET     | `/api/incidents/`                   | List all incidents       |
| GET     | `/api/incidents/{id}`               | Get single incident      |
| POST    | `/api/incidents/`                   | Create new incident      |
| PUT     | `/api/incidents/{id}`               | Update incident details  |
| PATCH   | `/api/incidents/{id}/acknowledge`   | Acknowledge incident     |
| PATCH   | `/api/incidents/{id}/escalate`      | Escalate incident        |
| PATCH   | `/api/incidents/{id}/resolve`       | Resolve incident         |
| DELETE  | `/api/incidents/{id}`               | Delete incident          |

### Alerts
| Method | Endpoint              | Description                          |
|--------|-----------------------|--------------------------------------|
| POST   | `/api/alerts`        | Ingest alert → auto-create incident  |

### WebSocket
- `ws://localhost:8000/ws` → Real-time incident updates

## Alert Ingestion Example
```json
POST /api/alerts
{
  "type": "server down",
  "message": "Production server web-01 is unreachable",
  "source": "infrastructure",
  "metadata": { "host": "web-01", "region": "us-east-1" }
}
```

## Incident Status Flow
```
NEW → ACKNOWLEDGED → RESOLVED
         ↘ ESCALATED ↗
```

## Deliverables Status:
- ✅ Gemini AI Classification Engine
- ✅ Multi-team Automatic Routing
- ✅ 3-Strike SLA Escalation Logic
- ✅ Real-time WebSocket Dashboard
- ✅ Automated Audit Logging

## Severity Levels
- `critical` — system down, data loss
- `high` — degraded performance, high error rate
- `medium` — warnings, minor issues
- `low` — informational, app-level errors
