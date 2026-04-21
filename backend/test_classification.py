from app.services.classification import classify_alert

# Test cases
alerts = [
    {"type": "server down", "source": "infrastructure"},
    {"type": "high cpu usage", "source": "infrastructure"},
    {"type": "api error", "source": "application"},
    {"type": "login slow", "source": "application"},
]

for alert in alerts:
    result = classify_alert(alert)
    print("Input:", alert)
    print("Output:", result)
    print("-" * 40)