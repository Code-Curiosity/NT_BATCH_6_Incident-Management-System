import './StatsBar.css';

function StatsBar({ incidents }) {
  const total = incidents.length;
  const critical = incidents.filter((i) => i.severity === 'critical').length;
  const open = incidents.filter((i) => i.status !== 'resolved').length;
  const resolved = incidents.filter((i) => i.status === 'resolved').length;

  const stats = [
    { label: 'Total', value: total, className: 'stat-total' },
    { label: 'Critical', value: critical, className: 'stat-critical' },
    { label: 'Open', value: open, className: 'stat-open' },
    { label: 'Resolved', value: resolved, className: 'stat-resolved' },
  ];

  return (
    <div className="stats-bar">
      {stats.map((stat) => (
        <div key={stat.label} className={`stat-card ${stat.className}`}>
          <span className="stat-value">{stat.value}</span>
          <span className="stat-label">{stat.label}</span>
        </div>
      ))}
    </div>
  );
}

export default StatsBar;
