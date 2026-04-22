import { useEffect, useState } from 'react';
import IncidentCard from '../components/IncidentCard.jsx';
import IncidentDetailsSidebar from '../components/IncidentDetailsSidebar.jsx';
import StatsBar from '../components/StatsBar.jsx';
import SideBar from '../components/SideBar.jsx';
import './Dashboard.css';

function Dashboard() {
  const [incidents, setIncidents] = useState([]);
  const [teams, setTeams] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [selectedTeam, setSelectedTeam] = useState('all');
  const [selectedUser, setSelectedUser] = useState('all');
  const [selectedIncident, setSelectedIncident] = useState(null);

  useEffect(() => {
    fetchInitialData();
  }, []);

  useEffect(() => {
    fetchIncidents();
  }, [filter, selectedTeam, selectedUser]);

  const fetchInitialData = async () => {
    try {
      const [teamsRes, usersRes] = await Promise.all([
        fetch('/api/teams/'),
        fetch('/api/users/')
      ]);
      setTeams(await teamsRes.json());
      setUsers(await usersRes.json());
    } catch (error) {
      console.error('Failed to fetch filter data:', error);
    }
  };

  const fetchIncidents = async () => {
    try {
      setLoading(true);
      let url = '/api/incidents/?';
      if (selectedTeam !== 'all') url += `team_id=${selectedTeam}&`;
      if (selectedUser !== 'all') url += `user_id=${selectedUser}&`;
      
      const response = await fetch(url);
      const data = await response.json();
      
      const fetchedIncidents = Array.isArray(data) ? data : (data.incidents || []);
      setIncidents(fetchedIncidents);
    } catch (error) {
      console.error('Failed to fetch incidents:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAction = async (incidentId, action) => {
    try {
      await fetch(`/api/incidents/${incidentId}/${action}`, { method: 'PATCH' });
      await fetchIncidents();
    } catch (error) {
      console.error(`Failed to ${action} incident:`, error);
    }
  };

  // Derive filtered + sorted list from state
  const filteredAndSortedIncidents = incidents
    .filter((inc) => {
      if (filter === 'all') return true;
      const s = (inc.status || '').toLowerCase();
      const f = filter.toLowerCase();
      // Map backend statuses to UI filter tabs
      if (f === 'new') return s === 'new' || s === 'open';
      return s === f;
    })
    .sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

  // Incidents considered "new" for sidebar badge count
  const newIncidents = incidents.filter(
    (inc) => {
      const s = (inc.status || '').toLowerCase();
      return s === 'new' || s === 'open';
    }
  );

  return (
    <div className="dashboard-shell">
      <SideBar newIncidents={newIncidents} />

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
          <div className="filter-group">
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

            <div className="dropdown-filters">
              <div className="filter-select-wrapper">
                <label htmlFor="team-filter">Team</label>
                <select
                  id="team-filter"
                  value={selectedTeam}
                  onChange={(e) => {
                    setSelectedTeam(e.target.value);
                    setSelectedUser('all');
                  }}
                >
                  <option value="all">All Teams</option>
                  {teams.map(team => (
                    <option key={team.id} value={team.id}>{team.name}</option>
                  ))}
                </select>
              </div>

              <div className="filter-select-wrapper">
                <label htmlFor="user-filter">User</label>
                <select
                  id="user-filter"
                  value={selectedUser}
                  onChange={(e) => setSelectedUser(e.target.value)}
                >
                  <option value="all">All Users</option>
                  {users
                    .filter(user => selectedTeam === 'all' || user.team_id === parseInt(selectedTeam))
                    .map(user => (
                      <option key={user.id} value={user.id}>{user.name}</option>
                    ))
                  }
                </select>
              </div>
            </div>
          </div>
        </div>

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
                onViewDetails={setSelectedIncident}
                teams={teams}
                users={users}
              />
            ))
          )}
        </main>

        {selectedIncident && (
          <IncidentDetailsSidebar
            incident={selectedIncident}
            onClose={() => setSelectedIncident(null)}
          />
        )}
      </div>
    </div>
  );
}

export default Dashboard;
