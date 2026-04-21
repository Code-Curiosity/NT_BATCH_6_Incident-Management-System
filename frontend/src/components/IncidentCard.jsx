import './IncidentCard.css';

function IncidentCard({ incident, onAction }) {
  const { id, title, description, severity, status, assigned_to, source, created_at } = incident;

  const formatTime = (isoString) => {
    if (!isoString) return '—';
    return new Date(isoString).toLocaleString();
  };

  return (
    <div className={`incident-card severity-${severity}`}>
      <div className="card-header">
        <span className={`severity-badge ${severity}`}>{severity.toUpperCase()}</span>
        <span className={`status-badge ${status}`}>{status}</span>
      </div>

      <h3 className="card-title">{title}</h3>
      {description && <p className="card-description">{description}</p>}

      <div className="card-meta">
        <div className="meta-item">
          <span className="meta-label">Assigned</span>
          <span className="meta-value">{assigned_to || 'Unassigned'}</span>
        </div>
        <div className="meta-item">
          <span className="meta-label">Source</span>
          <span className="meta-value">{source || '—'}</span>
        </div>
        <div className="meta-item">
          <span className="meta-label">Created</span>
          <span className="meta-value">{formatTime(created_at)}</span>
        </div>
      </div>

      <div className="card-actions">
        {status === 'new' && (
          <button className="action-btn acknowledge" onClick={() => onAction(id, 'acknowledge')}>
            Acknowledge
          </button>
        )}
        {(status === 'new' || status === 'acknowledged') && (
          <button className="action-btn escalate" onClick={() => onAction(id, 'escalate')}>
            Escalate
          </button>
        )}
        {status !== 'resolved' && (
          <button className="action-btn resolve" onClick={() => onAction(id, 'resolve')}>
            Resolve
          </button>
        )}
      </div>
    </div>
  );
}

export default IncidentCard;
