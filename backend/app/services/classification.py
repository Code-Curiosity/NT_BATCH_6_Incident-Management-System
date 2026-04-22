import json, os, re
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ── Fallback: Rule-based classifier ──────────────────────────────────────────
TYPE_RULES = {
    "SECURITY":       ["ssh", "brute force", "login attempt", "port scan", "certificate", "unauthorized", "suspicious", "attack", "firewall"],
    "PLATFORM":       ["kubernetes", "pod crash", "k8s", "pipeline", "ci/cd", "jenkins", "build failed", "deploy", "namespace", "helm"],
    "INFRASTRUCTURE": ["cpu", "disk", "memory", "oom", "server down", "database down", "network", "connection refused", "host down", "tcp", "db-prod"],
    "APPLICATION":    ["error rate", "exception", "api", "endpoint", "response time", "slow query", "500", "4xx", "timeout", "service"],
}

SEVERITY_RULES = {
    "CRITICAL": ["critical", "down", "outage", "crash", "connection refused", "oomkilled", "brute force", "unreachable"],
    "HIGH":     ["high", "spike", "exceeded", "95%", "94%", "93%", "failed", "4200ms", "18%"],
    "MEDIUM":   ["warning", "slow", "degraded", "elevated", "approaching threshold", "70%", "80%"],
    "LOW":      ["info", "low", "minor", "informational", "notice"],
}

PRIORITY_MAP = {"CRITICAL": 95, "HIGH": 70, "MEDIUM": 40, "LOW": 15}
SLA_MAP      = {"CRITICAL": 4,  "HIGH": 8,  "MEDIUM": 24, "LOW": 72}

def _rule_based_classify(raw_message: str, source: str) -> dict:
    msg = raw_message.lower()

    incident_type = "APPLICATION"
    for itype in ["SECURITY", "PLATFORM", "INFRASTRUCTURE", "APPLICATION"]:
        if any(kw in msg for kw in TYPE_RULES[itype]):
            incident_type = itype
            break

    severity = "MEDIUM"
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        if any(kw in msg for kw in SEVERITY_RULES[sev]):
            severity = sev
            break

    services = []
    for pattern in [r'\b[\w-]+-\d+\b', r'\b/api/[\w/]+\b', r'\b[\w-]+-service\b']:
        services.extend(re.findall(pattern, raw_message)[:2])

    title = re.sub(r'^\[?[A-Z]+\]?:?\s*', '', raw_message.split(".")[0].strip())[:80]
    description = (
        f"{incident_type.capitalize()} issue detected from {source}. "
        f"Severity assessed as {severity} based on alert content."
    )

    return {
        "title": title,
        "description": description,
        "severity": severity,
        "incident_type": incident_type,
        "affected_services": list(set(services))[:3] or [source],
        "priority_score": PRIORITY_MAP[severity],
        "sla_hours": SLA_MAP[severity],
    }

# ── Primary: Gemini classifier ────────────────────────────────────────────────
def classify_alert(raw_message: str, source: str) -> dict:
    prompt = f"""You are a DevOps incident classification engine.
Analyze this raw alert and return ONLY a valid JSON object. No markdown, no explanation.

Raw alert: {raw_message}
Source system: {source}

Return exactly this JSON structure:
{{
  "title": "short incident title under 80 chars",
  "description": "2 sentence explanation of what is happening and likely impact",
  "severity": "CRITICAL",
  "incident_type": "INFRASTRUCTURE",
  "affected_services": ["service1", "service2"],
  "priority_score": 95,
  "sla_hours": 4
}}

Severity must be one of: CRITICAL, HIGH, MEDIUM, LOW.
Incident_type must be one of: INFRASTRUCTURE, APPLICATION, PLATFORM, SECURITY.

Rules:
- INFRASTRUCTURE: server down, disk full, memory OOM, network failure, database crash
- APPLICATION: error rate spike, slow response, feature broken, failed deployment
- PLATFORM: CI/CD pipeline failure, Kubernetes issues, cloud resource exhaustion
- SECURITY: auth failures, suspicious logins, port scans, certificate expiry
- CRITICAL = sla_hours 4, HIGH = 8, MEDIUM = 24, LOW = 72
- priority_score: CRITICAL=90-100, HIGH=60-89, MEDIUM=30-59, LOW=1-29"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        text = response.text.strip().replace("```json", "").replace("```", "").strip()
        result = json.loads(text)
        
        # Enforce valid fields just in case LLM drifts
        if result.get("severity") not in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            result["severity"] = "MEDIUM"
            result["priority_score"] = 50
        if result.get("incident_type") not in ["INFRASTRUCTURE", "APPLICATION", "PLATFORM", "SECURITY"]:
            result["incident_type"] = "APPLICATION"
            
        return result
    except Exception as e:
        print(f"[Classifier] Gemini failed ({e}), using rule-based fallback")
        return _rule_based_classify(raw_message, source)