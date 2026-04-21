import { useEffect, useState } from 'react';
import IncidentCard from '../components/IncidentCard.jsx';
import IncidentDetailsSidebar from '../components/IncidentDetailsSidebar.jsx';
import StatsBar from '../components/StatsBar.jsx';
import SideBar from '../components/SideBar.jsx';
import './Dashboard.css';

function Dashboard() {
  const [incidents, setIncidents] = useState([]);
  const [selectedIncident, setSelectedIncident] = useState(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('created_at');
  const [sortOrder, setSortOrder] = useState('desc');
  const [theme, setTheme] = useState(() => localStorage.getItem('theme') || 'dark');

  useEffect(() => {
    fetchIncidents();
  }, []);

  useEffect(() => {
    document.body.className = `${theme}-theme`;
    localStorage.setItem('theme', theme);
  }, [theme]);

  const fetchIncidents = async () => {
    try {
      const response = await fetch('/api/incidents/');
      const data = await response.json();
      setIncidents(data);
    } catch (error) {
      console.error('Failed to fetch incidents:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAction = async (incidentId, action) => {
    try {
      await fetch(`/api/incidents/${incidentId}/${action}`, { method: 'PATCH' });
      fetchIncidents();
    } catch (error) {
      console.error(`Failed to ${action} incident:`, error);
    }
  };

  const resetView = () => {
    setSearchTerm('');
    setSortBy('created_at');
    setSortOrder('desc');
  };

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'));
  };

  const clearSearch = () => {
    setSearchTerm('');
  };

  const showNewIncidents = () => {
    setFilter('new');
    resetView();
  };

  const handleFilterChange = (nextFilter) => {
    setFilter(nextFilter);
  };

  const toggleSort = (field) => {
    if (sortBy === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(field);
      setSortOrder('desc');
    }
  };

  const newIncidents = incidents.filter((i) => i.status === 'new');

  const getPinnedPriority = (incident) =>
    incident.status === 'new' ? 0 : 1;

  const filteredAndSortedIncidents = incidents
    .filter((incident) =>
      filter === 'all'
        ? true
        : filter === 'active'
        ? incident.status !== 'resolved'
        : incident.status === filter
    )
    .filter((incident) =>
      searchTerm === '' ||
      incident.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      incident.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      incident.source?.toLowerCase().includes(searchTerm.toLowerCase())
    )
    .sort((a, b) => {
      if (filter === 'all') {
        const diff = getPinnedPriority(a) - getPinnedPriority(b);
        if (diff !== 0) return diff;
      }

      let aValue, bValue;

      switch (sortBy) {
        case 'severity': {
          const order = { critical: 4, high: 3, medium: 2, low: 1 };
          aValue = order[a.severity] || 0;
          bValue = order[b.severity] || 0;
          break;
        }
        case 'status': {
          const order = { new: 4, acknowledged: 3, escalated: 2, resolved: 1 };
          aValue = order[a.status] || 0;
          bValue = order[b.status] || 0;
          break;
        }
        default:
          aValue = new Date(a.created_at);
          bValue = new Date(b.created_at);
      }

      return sortOrder === 'asc'
        ? aValue > bValue ? 1 : -1
        : aValue < bValue ? 1 : -1;
    });

  return (
    <div className="dashboard-shell">

      {/* LEFT SIDEBAR */}
      <SideBar
        newIncidents={newIncidents}
      />

      {/* MAIN */}
      <div className="dashboard">

        {/* HEADER */}
        <header className="dashboard-header">
          <div className="header-content">
            <div className="header-main">
              <div>
                <p className="header-eyebrow">Incident Response Hub</p>
                <h1 className="header-title">
                  <img src="/favicon.png" alt="IncidentIQ" className="header-favicon" />
                  IncidentIQ
                </h1>
              </div>

              <div className="header-actions">
                <div className="live-badge">
                  <div className="live-dot"></div>
                  Live feed
                </div>

                <button
                  className={`bell-btn ${filter === 'new' ? 'active' : ''}`}
                  onClick={showNewIncidents}
                >
                  🔔
                  {newIncidents.length > 0 && (
                    <span className="notification-badge">
                      {newIncidents.length}
                    </span>
                  )}
                </button>

                <button className="theme-toggle-btn" onClick={toggleTheme}>
                  {theme === 'dark' ? '☀️' : '🌙'}
                </button>
              </div>
            </div>

            <p className="header-subtitle">
              Track incidents and respond in real time.
            </p>
          </div>
        </header>

        <StatsBar incidents={incidents} />

        {/* CONTROLS */}
        <div className="dashboard-controls">

          <div className="search-container">
            <div className="search-wrapper">
              <input
                type="text"
                placeholder="Search incidents..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="search-input"
              />
              {searchTerm && (
                <button className="clear-search-btn" onClick={clearSearch}>
                  ✕
                </button>
              )}
            </div>
          </div>

          <div className="controls-row">
            <div className="filter-tabs">
              {['all', 'new', 'acknowledged', 'escalated', 'resolved'].map((s) => (
                <button
                  key={s}
                  className={`filter-tab ${filter === s ? 'active' : ''}`}
                  onClick={() => handleFilterChange(s)}
                >
                  {s}
                </button>
              ))}

              <div className="sort-controls">
                <span className="sort-label">Sort by:</span>

                <button
                  className={`sort-btn ${sortBy === 'created_at' ? 'active' : ''}`}
                  onClick={() => toggleSort('created_at')}
                >
                  Date
                </button>

                <button
                  className={`sort-btn ${sortBy === 'severity' ? 'active' : ''}`}
                  onClick={() => toggleSort('severity')}
                >
                  Severity
                </button>

                <button
                  className={`sort-btn ${sortBy === 'status' ? 'active' : ''}`}
                  onClick={() => toggleSort('status')}
                >
                  Status
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* GRID */}
        <main className="incident-grid">
          {loading ? (
            <div className="loading-state">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="incident-card skeleton"></div>
              ))}
            </div>
          ) : filteredAndSortedIncidents.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">📋</div>
              <h3>No incidents found</h3>
              <p>Try adjusting your filters or search.</p>
            </div>
          ) : (
            filteredAndSortedIncidents.map((incident) => (
              <IncidentCard
                key={incident.id}
                incident={incident}
                onAction={handleAction}
                onViewDetails={setSelectedIncident}   // ✅ FIXED
              />
            ))
          )}
        </main>
      </div>

      {/* RIGHT DETAILS SIDEBAR */}
      {selectedIncident && (
        <IncidentDetailsSidebar
          incident={selectedIncident}
          onClose={() => setSelectedIncident(null)}
        />
      )}

    </div>
  );
}

export default Dashboard;
