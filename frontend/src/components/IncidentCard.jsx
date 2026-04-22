import { useState } from 'react';
import './IncidentCard.css';

const STATUS_FLOW = [
  {
    key: 'open',
    label: 'New',
    action: null,
    isAvailable: () => false,
  },
  {
    key: 'acknowledged',
    label: 'Acknowledge',
    action: 'acknowledge',
    isAvailable: (s) => s === 'open' || s === 'new',
  },
  {
    key: 'escalated',
    label: 'Escalate',
    action: 'escalate',
    isAvailable: (s) => ['open', 'new', 'acknowledged'].includes(s),
  },
  {
    key: 'resolved',
    label: 'Resolve',
    action: 'resolve',
    isAvailable: (s) => s !== 'resolved',
  },
];

function IncidentCard({ incident, onAction, onViewDetails, teams = [], users = [] }) {
  const {
    id,
    title,
    description,
    severity,
    status,
    source,
    created_at,
  } = incident;

  const [pendingAction, setPendingAction] = useState(null);

  const severityLower = severity ? severity.toLowerCase() : 'medium';
  const statusLower = status ? status.toLowerCase() : 'new';

  const formatTime = (iso) => {
    if (!iso) return '-';
    return new Date(iso).toLocaleString();
  };

  const handleStatusAction = async (action) => {
    if (!action || pendingAction) return;
    setPendingAction(action);
    try {
      await onAction(id, action);
    } finally {
      setPendingAction(null);
    }
  };

  // Resolve display names from teams/users arrays
  const teamName = teams.find(t => t.id === incident.assigned_team)?.name
    || incident.team_name || 'Unassigned';
  
  const matchedUser = users.find(u => u.id === incident.assigned_user);
  let userName = matchedUser?.name || incident.user_name || 'Unassigned';
  if (matchedUser?.role === 'lead') {
    userName += ' (Lead)';
  }

  return (
    <div className={`incident-card severity-${severityLower}`}>
      <div className="card-header">
        <span className={`severity-badge ${severityLower}`}>
          {severity ? severity.toUpperCase() : 'MEDIUM'}
        </span>
        <span className={`status-badge ${statusLower}`}>
          {status ? status.toUpperCase() : 'OPEN'}
        </span>
      </div>

      <h3 className="card-title">{title}</h3>
      {description && <p className="card-description">{description}</p>}

      <div className="card-status-flow">
        {STATUS_FLOW.map((step) => (
          <button
            key={step.key}
            className={`status-flow-chip ${
              statusLower === step.key
                ? 'current'
                : step.isAvailable(statusLower)
                ? 'available'
                : 'inactive'
            }`}
            onClick={() => handleStatusAction(step.action)}
            disabled={pendingAction || !step.isAvailable(statusLower)}
          >
            {pendingAction === step.action ? 'Updating...' : step.label}
          </button>
        ))}
      </div>

      <div className="card-meta">
        <div className="meta-item">
          <span className="meta-label">Team</span>
          <span className="meta-value">{teamName}</span>
        </div>
        <div className="meta-item">
          <span className="meta-label">Assignee</span>
          <span className="meta-value">{userName}</span>
        </div>
        <div className="meta-item">
          <span className="meta-label">Source</span>
          <span className="meta-value">{source || '-'}</span>
        </div>
        <div className="meta-item">
          <span className="meta-label">Created At</span>
          <span className="meta-value">{formatTime(created_at)}</span>
        </div>
        <div className="meta-item">
          <span className="meta-label">Updated At</span>
          <span className="meta-value">{incident.updated_at ? formatTime(incident.updated_at) : formatTime(created_at)}</span>
        </div>
      </div>

      <div className="card-actions">
        <button
          className="action-btn view-details"
          onClick={() => onViewDetails && onViewDetails(incident)}
        >
          View Details
        </button>
      </div>
    </div>
  );
}

export default IncidentCard;