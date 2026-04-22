import './StatsBar.css';

function StatsBar({ incidents }) {
  const total = incidents.length;
  const critical = incidents.filter((incident) => (incident.severity || '').toLowerCase() === 'critical').length;
  const open = incidents.filter((incident) => (incident.status || '').toLowerCase() !== 'resolved').length;
  const resolved = incidents.filter((incident) => (incident.status || '').toLowerCase() === 'resolved').length;

  const stats = [
    { label: 'Total Incidents', value: total, className: 'stat-total', icon: '\uD83D\uDCCB' },
    { label: 'Critical Active', value: critical, className: 'stat-critical', icon: '\u26A0\uFE0F' },
    { label: 'Open / Active', value: open, className: 'stat-open', icon: '\u23F1\uFE0F' },
    { label: 'Resolved Today', value: resolved, className: 'stat-resolved', icon: '\u2705' },
  ];

  return (
    <div className="stats-bar">
      {stats.map((stat) => (
        <div key={stat.label} className={`stat-card ${stat.className}`}>
          <div className="stat-icon">{stat.icon}</div>
          <div className="stat-value">{stat.value}</div>
          <div className="stat-label">{stat.label}</div>
        </div>
      ))}
    </div>
  );
}

export default StatsBar;
