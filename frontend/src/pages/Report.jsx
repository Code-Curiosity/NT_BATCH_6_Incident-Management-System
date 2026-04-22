import { useEffect, useRef, useState } from 'react';
import SideBar from '../components/SideBar.jsx';
import './Report.css';

const SEVERITY_ORDER = ['critical', 'high', 'medium', 'low'];
const STATUS_ORDER = ['new', 'acknowledged', 'escalated', 'resolved'];
const REPORT_DAYS = 7;

const CHART_COLORS = {
  critical: '#ef4444',
  high: '#f59e0b',
  medium: '#eab308',
  low: '#22c55e',
  new: '#3b82f6',
  acknowledged: '#8b5cf6',
  escalated: '#f97316',
  resolved: '#10b981',
  infrastructure: '#38bdf8',
  application: '#f472b6',
  default: '#64748b',
};

const DONUT_PALETTES = {
  severity: {
    critical: '#ef4444',
    high: '#f9d716',
    medium: '#facc15',
    low: '#22c55e',
    default: '#64748b',
  },
  status: {
    new: '#06b6d4',
    acknowledged: '#f6dc5c',
    escalated: '#f8072f',
    resolved: '#06a91c',
    default: '#64748b',
  },
};

function formatLabel(value) {
  return String(value)
    .split(/[_\s-]+/)
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ');
}

function groupCounts(items, keySelector, preferredOrder = []) {
  const counts = new Map();

  items.forEach((item) => {
    const key = keySelector(item) || 'unknown';
    counts.set(key, (counts.get(key) || 0) + 1);
  });

  const ordered = [];
  preferredOrder.forEach((key) => {
    if (counts.has(key)) {
      ordered.push({ key, label: formatLabel(key), value: counts.get(key) });
      counts.delete(key);
    }
  });

  Array.from(counts.entries())
    .sort((a, b) => b[1] - a[1])
    .forEach(([key, value]) => {
      ordered.push({ key, label: formatLabel(key), value });
    });

  return ordered;
}

function buildCsv(incidents) {
  const rows = [
    ['ID', 'Title', 'Severity', 'Status', 'Assigned To', 'Source', 'Created At', 'Updated At', 'Description'],
    ...incidents.map((incident) => [
      incident.id,
      incident.title,
      incident.severity,
      incident.status,
      incident.assigned_to || '',
      incident.source || '',
      incident.created_at || '',
      incident.updated_at || '',
      incident.description || '',
    ]),
  ];

  return rows
    .map((row) => row.map((cell) => `"${String(cell).replaceAll('"', '""')}"`).join(','))
    .join('\n');
}

function buildSummaryText(summary) {
  const lines = [
    'IncidentIQ Operations Report',
    `Generated: ${new Date().toLocaleString()}`,
    '',
    `Total incidents: ${summary.totalIncidents}`,
    `Open incidents: ${summary.openIncidents}`,
    `Resolved incidents: ${summary.resolvedIncidents}`,
    `Critical active incidents: ${summary.criticalActive}`,
    `Resolution rate: ${summary.resolutionRate}%`,
    `Average close time: ${summary.averageResolutionHours} hrs`,
    `Top weekly assignee: ${summary.topWeeklyAssignee.label} (${summary.topWeeklyAssignee.value})`,
    '',
    'Severity distribution:',
    ...summary.severityBreakdown.map((item) => `- ${item.label}: ${item.value}`),
    '',
    'Status distribution:',
    ...summary.statusBreakdown.map((item) => `- ${item.label}: ${item.value}`),
    '',
    'Source distribution:',
    ...summary.sourceBreakdown.map((item) => `- ${item.label}: ${item.value}`),
    '',
    'Top assignments:',
    ...summary.assignmentBreakdown.slice(0, 5).map((item) => `- ${item.label}: ${item.value}`),
  ];

  return lines.join('\n');
}

function downloadFile(filename, content, type) {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

function buildDonutSegments(items, palette = CHART_COLORS) {
  const total = items.reduce((sum, item) => sum + item.value, 0) || 1;
  let currentAngle = 0;

  return items.map((item) => {
    const segmentAngle = (item.value / total) * 360;
    const start = currentAngle;
    currentAngle += segmentAngle;

    return {
      ...item,
      color: palette[item.key] || palette.default || CHART_COLORS.default,
      start,
      end: currentAngle,
      percent: Math.round((item.value / total) * 100),
    };
  });
}

function buildTrendData(incidents, dateKey) {
  const days = [];
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  // Helper to reliably get YYYY-MM-DD in the local timezone
  const getLocalDateKey = (dateObj) => {
    const year = dateObj.getFullYear();
    const month = String(dateObj.getMonth() + 1).padStart(2, '0');
    const day = String(dateObj.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  };

  for (let index = REPORT_DAYS - 1; index >= 0; index -= 1) {
    const day = new Date(today);
    day.setDate(today.getDate() - index);
    days.push({
      key: getLocalDateKey(day),
      label: day.toLocaleDateString([], { weekday: 'short' }),
      value: 0,
    });
  }

  const lookup = new Map(days.map((day) => [day.key, day]));
  incidents.forEach((incident) => {
    const dateValue = incident[dateKey];
    if (!dateValue) {
      return;
    }

    const key = getLocalDateKey(new Date(dateValue));
    if (lookup.has(key)) {
      lookup.get(key).value += 1;
    }
  });

  return days;
}

function calculateSummary(incidents) {
  const weekStart = new Date();
  weekStart.setHours(0, 0, 0, 0);
  weekStart.setDate(weekStart.getDate() - (REPORT_DAYS - 1));

  const totalIncidents = incidents.length;
  const openIncidents = incidents.filter((incident) => incident.status !== 'resolved').length;
  const resolvedIncidents = incidents.filter((incident) => incident.status === 'resolved').length;
  const criticalActive = incidents.filter(
    (incident) => incident.severity === 'critical' && incident.status !== 'resolved',
  ).length;
  const resolutionRate = totalIncidents === 0
    ? 0
    : Math.round((resolvedIncidents / totalIncidents) * 100);

  const resolutionHours = incidents
    .filter((incident) => incident.status === 'resolved' && incident.created_at && incident.updated_at)
    .map((incident) => (
      (new Date(incident.updated_at).getTime() - new Date(incident.created_at).getTime()) / 3600000
    ));

  const averageResolutionHours = resolutionHours.length === 0
    ? 0
    : (resolutionHours.reduce((sum, value) => sum + value, 0) / resolutionHours.length).toFixed(1);

  const severityBreakdown = groupCounts(incidents, (incident) => incident.severity, SEVERITY_ORDER);
  const statusBreakdown = groupCounts(incidents, (incident) => incident.status, STATUS_ORDER);
  const sourceBreakdown = groupCounts(incidents, (incident) => incident.source || 'unknown');
  const assignmentBreakdown = groupCounts(incidents, (incident) => incident.assigned_to || 'unassigned');
  const weeklyAssignmentBreakdown = groupCounts(
    incidents.filter((incident) => (
      incident.assigned_to
      && incident.created_at
      && new Date(incident.created_at) >= weekStart
    )),
    (incident) => incident.assigned_to,
  );
  const topWeeklyAssignee = weeklyAssignmentBreakdown[0] || {
    key: 'none',
    label: 'No assignee',
    value: 0,
  };
  const incidentTrend = buildTrendData(incidents, 'created_at');
  const resolutionTrend = buildTrendData(
    incidents.filter((incident) => incident.status === 'resolved'),
    'updated_at',
  );

  const newestFirst = [...incidents].sort(
    (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime(),
  );

  return {
    totalIncidents,
    openIncidents,
    resolvedIncidents,
    criticalActive,
    resolutionRate,
    averageResolutionHours,
    severityBreakdown,
    statusBreakdown,
    sourceBreakdown,
    assignmentBreakdown,
    weeklyAssignmentBreakdown,
    topWeeklyAssignee,
    incidentTrend,
    resolutionTrend,
    recentIncidents: newestFirst.slice(0, 6),
  };
}

function DonutChart({ title, items, centerLabel, palette }) {
  const segments = buildDonutSegments(items, palette);
  const gradient = segments.length === 0
    ? 'conic-gradient(#cbd5e1 0deg 360deg)'
    : `conic-gradient(${segments.map((segment) => (
      `${segment.color} ${segment.start}deg ${segment.end}deg`
    )).join(', ')})`;

  return (
    <section className="report-panel donut-panel">
      <div className="report-panel-header">
        <div>
          <span className="report-panel-kicker">Distribution</span>
          <h3>{title}</h3>
        </div>
      </div>

      <div className="donut-layout">
        <div className="donut-chart" style={{ backgroundImage: gradient }}>
          <div className="donut-hole">
            <strong>{centerLabel}</strong>
            <span>Total</span>
          </div>
        </div>

        <div className="donut-legend">
          {segments.map((segment) => (
            <div key={segment.key} className="legend-row">
              <span className="legend-swatch" style={{ backgroundColor: segment.color }}></span>
              <span className="legend-label">{segment.label}</span>
              <span className="legend-value">{segment.value}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function BarListChart({ title, kicker, items }) {
  const maxValue = Math.max(...items.map((item) => item.value), 1);

  return (
    <section className="report-panel">
      <div className="report-panel-header">
        <div>
          <span className="report-panel-kicker">{kicker}</span>
          <h3>{title}</h3>
        </div>
      </div>

      <div className="bar-list">
        {items.map((item) => (
          <div key={item.key} className="bar-list-row">
            <div className="bar-list-meta">
              <span>{item.label}</span>
              <strong>{item.value}</strong>
            </div>
            <div className="bar-track">
              <div
                className="bar-fill"
                style={{
                  width: `${(item.value / maxValue) * 100}%`,
                  background: `linear-gradient(90deg, ${CHART_COLORS[item.key] || CHART_COLORS.default}, rgba(59, 130, 246, 0.25))`,
                }}
              ></div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

function TrendChart({ title, kicker, items, lineColor }) {
  const width = 520;
  const height = 200;
  const padding = 26;
  const maxValue = Math.max(...items.map((item) => item.value), 1);
  const stepX = items.length > 1 ? (width - padding * 2) / (items.length - 1) : 0;

  const points = items.map((item, index) => {
    const x = padding + index * stepX;
    const y = height - padding - ((item.value / maxValue) * (height - padding * 2));
    return { ...item, x, y };
  });

  const linePath = points.map((point, index) => `${index === 0 ? 'M' : 'L'} ${point.x} ${point.y}`).join(' ');
  const areaPath = `${linePath} L ${points[points.length - 1]?.x || padding} ${height - padding} L ${points[0]?.x || padding} ${height - padding} Z`;

  return (
    <section className="report-panel trend-panel">
      <div className="report-panel-header">
        <div>
          <span className="report-panel-kicker">{kicker}</span>
          <h3>{title}</h3>
        </div>
      </div>

      <svg viewBox={`0 0 ${width} ${height}`} className="trend-chart" role="img" aria-label={title}>
        <defs>
          <linearGradient id={`${title.replace(/\s+/g, '-')}-gradient`} x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={lineColor} stopOpacity="0.35" />
            <stop offset="100%" stopColor={lineColor} stopOpacity="0.02" />
          </linearGradient>
        </defs>

        {[0, 1, 2, 3].map((line) => {
          const y = padding + ((height - padding * 2) / 3) * line;
          return (
            <line
              key={line}
              x1={padding}
              y1={y}
              x2={width - padding}
              y2={y}
              className="trend-grid-line"
            />
          );
        })}

        <path d={areaPath} fill={`url(#${title.replace(/\s+/g, '-')}-gradient)`} />
        <path d={linePath} fill="none" stroke={lineColor} strokeWidth="3" strokeLinecap="round" />

        {points.map((point) => (
          <g key={point.key}>
            <circle cx={point.x} cy={point.y} r="5" fill={lineColor} className="trend-point" />
            <text x={point.x} y={height - 6} textAnchor="middle" className="trend-label">
              {point.label}
            </text>
            <text x={point.x} y={point.y - 10} textAnchor="middle" className="trend-value">
              {point.value}
            </text>
          </g>
        ))}
      </svg>
    </section>
  );
}

function Report() {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [theme, setTheme] = useState(() => localStorage.getItem('theme') || 'dark');
  const [isExportMenuOpen, setIsExportMenuOpen] = useState(false);
  const exportMenuRef = useRef(null);

  useEffect(() => {
    fetchIncidents();
  }, []);

  useEffect(() => {
    document.body.className = `${theme}-theme`;
    localStorage.setItem('theme', theme);
  }, [theme]);

  useEffect(() => {
    const handlePointerDown = (event) => {
      if (exportMenuRef.current && !exportMenuRef.current.contains(event.target)) {
        setIsExportMenuOpen(false);
      }
    };

    const handleEscape = (event) => {
      if (event.key === 'Escape') {
        setIsExportMenuOpen(false);
      }
    };

    document.addEventListener('mousedown', handlePointerDown);
    document.addEventListener('keydown', handleEscape);

    return () => {
      document.removeEventListener('mousedown', handlePointerDown);
      document.removeEventListener('keydown', handleEscape);
    };
  }, []);

  const [users, setUsers] = useState([]);

  const fetchIncidents = async () => {
    try {
      const [incRes, usersRes] = await Promise.all([
        fetch('/api/incidents/'),
        fetch('/api/users/')
      ]);
      const data = await incRes.json();
      const userData = await usersRes.json();
      setUsers(userData);

      const raw = Array.isArray(data) ? data : (data.incidents || []);
      const normalized = raw.map(inc => {
        // Find the user to map ID -> Name
        const assignee = userData.find(u => u.id === inc.assigned_user || u.id === inc.assigned_to);
        const assigneeName = assignee ? assignee.name : (inc.assigned_user || 'unassigned');
        
        return {
          ...inc,
          severity: (inc.severity || 'medium').toLowerCase(),
          status: (inc.status || 'new').toLowerCase().replace('open', 'new'),
          assigned_to: assigneeName,
        };
      });
      setIncidents(normalized);
    } catch (error) {
      console.error('Failed to fetch report incidents:', error);
    } finally {
      setLoading(false);
    }
  };

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'));
  };

  const summary = calculateSummary(incidents);
  const newIncidents = incidents.filter((incident) => incident.status === 'new');

  const downloadCsv = () => {
    setIsExportMenuOpen(false);
    downloadFile('incident-report.csv', buildCsv(incidents), 'text/csv;charset=utf-8');
  };

  const downloadJson = () => {
    setIsExportMenuOpen(false);
    downloadFile(
      'incident-report.json',
      JSON.stringify(
        {
          generated_at: new Date().toISOString(),
          summary,
          incidents,
        },
        null,
        2,
      ),
      'application/json;charset=utf-8',
    );
  };

  const downloadSummary = () => {
    setIsExportMenuOpen(false);
    downloadFile(
      'incident-summary.txt',
      buildSummaryText(summary),
      'text/plain;charset=utf-8',
    );
  };

  return (
    <div className="report-shell">
      <SideBar newIncidents={newIncidents} />

      <main className="report-page">
        <header className="report-header">
          <div className="report-header-copy">
            <span className="report-eyebrow">Analytics Console</span>
            <h1>Incident Reports</h1>
            <p>
              Explore incident health, workload shifts, severity patterns, and download
              snapshots your team can share outside the dashboard.
            </p>
          </div>

          <div className="report-header-actions">
            <button type="button" className="report-theme-btn" onClick={toggleTheme}>
              {theme === 'dark' ? '\u2600\uFE0F' : '\uD83C\uDF19'}
            </button>
            <button type="button" className="report-download-btn primary" onClick={downloadSummary}>
              Download Summary
            </button>
            <div className="report-dropdown" ref={exportMenuRef}>
              <button
                type="button"
                className={`report-download-btn report-dropdown-trigger ${isExportMenuOpen ? 'open' : ''}`}
                onClick={() => setIsExportMenuOpen((open) => !open)}
                aria-haspopup="menu"
                aria-expanded={isExportMenuOpen}
              >
                Export Data
                <span className="report-dropdown-caret" aria-hidden="true">
                  {isExportMenuOpen ? '\u25B2' : '\u25BE'}
                </span>
              </button>

              {isExportMenuOpen && (
                <div className="report-dropdown-menu" role="menu" aria-label="Export data">
                  <button
                    type="button"
                    className="report-dropdown-item"
                    onClick={downloadCsv}
                    role="menuitem"
                  >
                    Export CSV
                  </button>
                  <button
                    type="button"
                    className="report-dropdown-item"
                    onClick={downloadJson}
                    role="menuitem"
                  >
                    Export JSON
                  </button>
                </div>
              )}
            </div>
          </div>
        </header>

        {loading ? (
          <section className="report-loading">
            <div className="report-loading-grid">
              {[...Array(6)].map((_, index) => (
                <div key={index} className="report-skeleton-card"></div>
              ))}
            </div>
          </section>
        ) : (
          <>
            <section className="report-overview-grid">
              <article className="report-stat-card total">
                <span className="report-stat-label">Total Incidents</span>
                <strong>{summary.totalIncidents}</strong>
                <p>All incidents captured in the current workspace.</p>
              </article>

              <article className="report-stat-card active">
                <span className="report-stat-label">Open Incidents</span>
                <strong>{summary.openIncidents}</strong>
                <p>Incidents still active across new, acknowledged, or escalated states.</p>
              </article>

              <article className="report-stat-card critical">
                <span className="report-stat-label">Critical Active</span>
                <strong>{summary.criticalActive}</strong>
                <p>Highest-risk incidents still requiring action.</p>
              </article>

              <article className="report-stat-card resolved">
                <span className="report-stat-label">Resolution Rate</span>
                <strong>{summary.resolutionRate}%</strong>
                <p>Resolved share of all tracked incidents.</p>
              </article>

              <article className="report-stat-card assignee">
                <span className="report-stat-label">Top Weekly Assignee</span>
                <strong>{summary.topWeeklyAssignee.label}</strong>
                <p>
                  {summary.topWeeklyAssignee.value > 0
                    ? `${summary.topWeeklyAssignee.value} assigned this week`
                    : 'No assigned incidents in the last 7 days.'}
                </p>
              </article>
            </section>

            <section className="report-chart-grid">
              <DonutChart
                title="Severity Split"
                items={summary.severityBreakdown}
                centerLabel={String(summary.totalIncidents)}
                palette={DONUT_PALETTES.severity}
              />
              <DonutChart
                title="Status Split"
                items={summary.statusBreakdown}
                centerLabel={String(summary.openIncidents)}
                palette={DONUT_PALETTES.status}
              />
              <TrendChart
                title="Incident Intake"
                kicker="Last 7 Days"
                items={summary.incidentTrend}
                lineColor="#3b82f6"
              />
              <TrendChart
                title="Resolutions"
                kicker="Last 7 Days"
                items={summary.resolutionTrend}
                lineColor="#10b981"
              />
              <BarListChart
                title="Source Mix"
                kicker="Incoming Channels"
                items={summary.sourceBreakdown}
              />
              <BarListChart
                title="Assignment Load"
                kicker="Top Owners"
                items={summary.assignmentBreakdown.slice(0, 6)}
              />
            </section>

            <section className="report-bottom-grid">
              <section className="report-panel narrative-panel">
                <div className="report-panel-header">
                  <div>
                    <span className="report-panel-kicker">Executive Summary</span>
                    <h3>Operations Snapshot</h3>
                  </div>
                </div>

                <div className="narrative-list">
                  <div className="narrative-item">
                    <strong>{summary.criticalActive}</strong>
                    <p>critical incidents remain active and should stay at the top of the response queue.</p>
                  </div>
                  <div className="narrative-item">
                    <strong>{summary.averageResolutionHours} hrs</strong>
                    <p>is the current average close time for resolved incidents in this dataset.</p>
                  </div>
                  <div className="narrative-item">
                    <strong>{summary.sourceBreakdown[0]?.label || 'No source'}</strong>
                    <p>is the busiest source channel based on the incidents currently recorded.</p>
                  </div>
                  <div className="narrative-item">
                    <strong>{summary.topWeeklyAssignee.label}</strong>
                    <p>
                      {summary.topWeeklyAssignee.value > 0
                        ? `received the most assignments this week with ${summary.topWeeklyAssignee.value} incidents.`
                        : 'has not received any new assignments in the last 7 days.'}
                    </p>
                  </div>
                </div>
              </section>

              <section className="report-panel recent-incidents-panel">
                <div className="report-panel-header">
                  <div>
                    <span className="report-panel-kicker">Recent Activity</span>
                    <h3>Latest Incidents</h3>
                  </div>
                </div>

                <div className="recent-incident-table">
                  {summary.recentIncidents.map((incident) => (
                    <div key={incident.id} className="recent-incident-row">
                      <div className="recent-incident-main">
                        <strong>{incident.title}</strong>
                        <span>#{incident.id}</span>
                      </div>
                      <div className="recent-incident-meta">
                        <span className={`report-chip severity ${incident.severity}`}>
                          {formatLabel(incident.severity)}
                        </span>
                        <span className={`report-chip status ${incident.status}`}>
                          {formatLabel(incident.status)}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </section>
            </section>
          </>
        )}
      </main>
    </div>
  );
}

export default Report;
