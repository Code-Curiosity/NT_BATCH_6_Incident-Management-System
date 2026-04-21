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
| POST   | `/api/alerts/ingest`  | Ingest alert → auto-create incident  |

### WebSocket
- `ws://localhost:8000/ws` → Real-time incident updates

## Alert Ingestion Example
```json
POST /api/alerts/ingest
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

## Severity Levels
- `critical` — system down, data loss
- `high` — degraded performance, high error rate
- `medium` — warnings, minor issues
- `low` — informational, app-level errors
