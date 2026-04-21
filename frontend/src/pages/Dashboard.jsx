import { useState, useEffect } from 'react';
import IncidentCard from '../components/IncidentCard.jsx';
import StatsBar from '../components/StatsBar.jsx';
import './Dashboard.css';

function Dashboard() {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // all, new, acknowledged, escalated, resolved

  useEffect(() => {
    fetchIncidents();
    // TODO: Connect WebSocket for real-time updates
  }, []);

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
      fetchIncidents(); // Refresh after action
    } catch (error) {
      console.error(`Failed to ${action} incident:`, error);
    }
  };

  const filteredIncidents = filter === 'all'
    ? incidents
    : incidents.filter((inc) => inc.status === filter);

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-content">
          <h1 className="header-title">
            <span className="header-icon">🔴</span>
            Incident Management
          </h1>
          <p className="header-subtitle">Real-time DevOps incident tracking & resolution</p>
        </div>
      </header>

      <StatsBar incidents={incidents} />

      <div className="dashboard-controls">
        <div className="filter-tabs">
          {['all', 'new', 'acknowledged', 'escalated', 'resolved'].map((status) => (
            <button
              key={status}
              className={`filter-tab ${filter === status ? 'active' : ''}`}
              onClick={() => setFilter(status)}
            >
              {status.charAt(0).toUpperCase() + status.slice(1)}
            </button>
          ))}
        </div>
      </div>

      <main className="incident-grid">
        {loading ? (
          <div className="loading-state">Loading incidents...</div>
        ) : filteredIncidents.length === 0 ? (
          <div className="empty-state">No incidents found.</div>
        ) : (
          filteredIncidents.map((incident) => (
            <IncidentCard
              key={incident.id}
              incident={incident}
              onAction={handleAction}
            />
          ))
        )}
      </main>
    </div>
  );
}

export default Dashboard;
