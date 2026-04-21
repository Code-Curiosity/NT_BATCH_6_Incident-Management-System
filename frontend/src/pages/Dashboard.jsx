import { useState, useEffect } from 'react';
import IncidentCard from '../components/IncidentCard.jsx';
import StatsBar from '../components/StatsBar.jsx';
import './Dashboard.css';

function Dashboard() {
  const [incidents, setIncidents] = useState([]);
  const [teams, setTeams] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // all, new, acknowledged, escalated, resolved
  const [selectedTeam, setSelectedTeam] = useState('all');
  const [selectedUser, setSelectedUser] = useState('all');

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
      
      const fetchedIncidents = data.incidents || data;
      
      // Client-side filtering for status since we already have the data
      // or we could add status to the API. For now, let's keep status filtering client-side
      // to avoid over-complicating the backend query logic if not needed.
      const statusFiltered = filter === 'all' 
        ? fetchedIncidents 
        : fetchedIncidents.filter(inc => inc.status.toLowerCase() === filter.toLowerCase() || inc.status.toLowerCase() === (filter === 'new' ? 'open' : filter));
        
      setIncidents(statusFiltered);
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
                  setSelectedUser('all'); // Reset user when team changes
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
          <div className="loading-state">Loading incidents...</div>
        ) : incidents.length === 0 ? (
          <div className="empty-state">No incidents found.</div>
        ) : (
          incidents.map((incident) => (
            <IncidentCard
              key={incident.id}
              incident={incident}
              onAction={handleAction}
              teams={teams}
              users={users}
            />
          ))
        )}
      </main>
    </div>
  );
}

export default Dashboard;
