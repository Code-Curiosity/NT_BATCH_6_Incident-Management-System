import { useState } from 'react';
import './IncidentCard.css';

function IncidentCard({ incident, onAction, teams=[], users=[] }) {
  const { id, title, description, severity, status, source, created_at } = incident;

function IncidentCard({ incident, onAction, onViewDetails }) {
  const {
    id,
    title,
    description,
    severity,
    status,
    assigned_to,
    source,
    created_at,
  } = incident;

  const [pendingAction, setPendingAction] = useState(null);

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

  return (
    <div className={`incident-card severity-${severity}`}>
      <div className="card-header">
        <span className={`severity-badge ${severity}`}>
          {severity.toUpperCase()}
        </span>
        <span className={`status-badge ${status}`}>{status}</span>
      </div>

      <h3 className="card-title">{title}</h3>
      {description && <p className="card-description">{description}</p>}

      <div className="card-status-flow">
        {STATUS_FLOW.map((step) => (
          <button
            key={step.key}
            className={`status-flow-chip ${
              status === step.key
                ? 'current'
                : step.isAvailable(status)
                ? 'available'
                : 'inactive'
            }`}
            onClick={() => handleStatusAction(step.action)}
            disabled={pendingAction || !step.isAvailable(status)}
          >
            {pendingAction === step.action ? 'Updating...' : step.label}
          </button>
        ))}
      </div>

      <div className="card-meta">
        <div className="meta-item">
          <span className="meta-label">Team</span>
          <span className="meta-value">{teams.find(t => t.id === incident.assigned_team)?.name || incident.team_name || 'Unassigned'}</span>
        </div>
        <div className="meta-item">
          <span className="meta-label">Assignee</span>
          <span className="meta-value">{users.find(u => u.id === incident.assigned_user)?.name || incident.user_name || 'Unassigned'}</span>
        </div>
        <div className="meta-item">
          <span className="meta-label">Assigned to</span>
          <span className="meta-value">{ 'Person Name'}</span>
        </div>
        <div className="meta-item">
          <span className="meta-label">Source</span>
          <span className="meta-value">{source || '-'}</span>
        </div>
        <div className="meta-item">
          <span className="meta-label">Created</span>
          <span className="meta-value">{formatTime(created_at)}</span>
        </div>
      </div>

      <div className="card-actions">
        <button
          className="action-btn view-details"
          onClick={() => onViewDetails(incident)}
        >
          View Details
        </button>
      </div>
    </div>
  );
}

export default IncidentCard;