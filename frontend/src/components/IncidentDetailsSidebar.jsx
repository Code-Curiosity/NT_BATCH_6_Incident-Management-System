import React, { useState, useEffect } from 'react';
import './IncidentDetailsSidebar.css';
const SEVERITY_COPY = {
  critical: {
    badge: 'Critical',
    pulse: 'Immediate response window',
    icon: '\u26A0',
  },
  high: {
    badge: 'High',
    pulse: 'Fast follow-up required',
    icon: '\u25B2',
  },
  medium: {
    badge: 'Medium',
    pulse: 'Monitor and stabilize',
    icon: '\u25C8',
  },
  low: {
    badge: 'Low',
    pulse: 'Routine observation track',
    icon: '\u25CF',
  },
};

const STATUS_COPY = {
  new: { label: 'New', note: 'Awaiting first response' },
  acknowledged: { label: 'Acknowledged', note: 'Assigned and under review' },
  escalated: { label: 'Escalated', note: 'Needs wider attention' },
  resolved: { label: 'Resolved', note: 'Closed and stabilized' },
};

function IncidentDetailsSidebar({ incident, onClose, users = [] }) {
  if (!incident) return null;

  const sevKey = (incident.severity || 'low').toLowerCase();
  const statKey = (incident.status || 'new').toLowerCase().replace('open', 'new');
  
  const assignedUserObj = users.find(u => u.id === incident.assigned_user);
  const assigneeName = assignedUserObj ? assignedUserObj.name : 'Unassigned';
  const severityMeta = SEVERITY_COPY[sevKey] || SEVERITY_COPY.low;
  const statusMeta = STATUS_COPY[statKey] || STATUS_COPY.new;

  const formatTime = (iso) => {
    if (!iso) return '-';
    return new Date(iso).toLocaleString();
  };

  const formatRelativeTime = (iso) => {
    if (!iso) return 'No timestamp';

    const timestamp = new Date(iso).getTime();
    const deltaMs = Date.now() - timestamp;
    const minutes = Math.max(1, Math.round(deltaMs / 60000));

    if (minutes < 60) {
      return `${minutes}m ago`;
    }

    const hours = Math.round(minutes / 60);
    if (hours < 24) {
      return `${hours}h ago`;
    }

    const days = Math.round(hours / 24);
    return `${days}d ago`;
  };

  const [logs, setLogs] = useState([]);

  useEffect(() => {
    if (incident?.id) {
      fetch(`/api/incidents/${incident.id}`)
        .then((res) => res.json())
        .then((data) => setLogs(data.logs || []))
        .catch(err => console.error("Could not fetch logs:", err));
    }
  }, [incident]);

  const detailItems = [
    { label: 'Assignment', value: assigneeName },
    { label: 'Source', value: incident.source || 'Unknown source' },
    { label: 'Created', value: formatTime(incident.created_at) },
    { label: 'Last update', value: formatTime(incident.updated_at) },
  ];

  const timelineItems = logs.length > 0 ? logs.map(log => ({
    label: log.action.charAt(0) + log.action.slice(1).toLowerCase(),
    time: formatTime(log.timestamp),
    note: log.details,
    tone: log.action.toLowerCase(),
  })) : [
    {
      label: 'Signal received',
      time: formatTime(incident.created_at),
      note: `Incident opened ${formatRelativeTime(incident.created_at)}`,
      tone: 'created',
    }
  ];

  return (
    <div className="details-sidebar-layer">
      <button
        type="button"
        className="details-sidebar-backdrop"
        onClick={onClose}
        aria-label="Close incident details"
      />

      <aside
        className={`details-sidebar severity-${sevKey}`}
        aria-label={`Details for incident ${incident.id}`}
      >
        <div className="details-hero">
          <div className="details-header">
            <div>
              <p className="details-eyebrow">Incident Details</p>
              <p className="details-case-id">Case #{incident.id}</p>
            </div>
            <button
              type="button"
              className="details-close-btn"
              onClick={onClose}
              aria-label="Close details panel"
            >
              {'\u2715'}
            </button>
          </div>

          <div className="details-hero-body">
            <div className="details-hero-copy">
              <h2>{incident.title}</h2>
              <p className="details-summary">{severityMeta.pulse}</p>
            </div>
            <div className="details-signal-orb" aria-hidden="true">
              <span>{severityMeta.icon}</span>
            </div>
          </div>

          <div className="details-pill-row">
            <span className={`details-pill severity ${sevKey}`}>
              {severityMeta.badge}
            </span>
            <span className={`details-pill status ${statKey}`}>
              {statusMeta.label}
            </span>
            <span className="details-pill neutral">
              {formatRelativeTime(incident.created_at)}
            </span>
          </div>
        </div>

        <div className="details-content">
          <section className="details-panel details-metrics-grid">
            {detailItems.map((item) => (
              <div key={item.label} className="details-metric-card">
                <span className="details-metric-label">{item.label}</span>
                <span className="details-metric-value">{item.value}</span>
              </div>
            ))}
          </section>

          <section className="details-panel">
            <div className="details-section-header">
              <span className="details-section-kicker">Status Readout</span>
              <h3>Response posture</h3>
            </div>
            <div className="details-insight-grid">
              <div className="details-insight-card">
                <span className="details-insight-label">Severity signal</span>
                <strong>{severityMeta.badge}</strong>
                <p>{severityMeta.pulse}</p>
              </div>
              <div className="details-insight-card">
                <span className="details-insight-label">Operational state</span>
                <strong>{statusMeta.label}</strong>
                <p>{statusMeta.note}</p>
              </div>
            </div>
          </section>

          <section className="details-panel">
            <div className="details-section-header">
              <span className="details-section-kicker">Activity Trail</span>
              <h3>Timeline</h3>
            </div>
            <div className="details-timeline">
              {timelineItems.map((item) => (
                <div key={item.label} className="details-timeline-item">
                  <div className={`details-timeline-dot ${item.tone}`}></div>
                  <div className="details-timeline-copy">
                    <div className="details-timeline-row">
                      <span className="details-timeline-title">{item.label}</span>
                      <span className="details-timeline-time">{item.time}</span>
                    </div>
                    <p>{item.note}</p>
                  </div>
                </div>
              ))}
            </div>
          </section>

          <section className="details-panel">
            <div className="details-section-header">
              <span className="details-section-kicker">Description</span>
              <h3>Incident narrative</h3>
            </div>
            <div className="details-description-card">
              <p>{incident.description || 'No description has been recorded for this incident yet.'}</p>
            </div>
          </section>
        </div>
      </aside>
    </div>
  );
}

export default IncidentDetailsSidebar;
