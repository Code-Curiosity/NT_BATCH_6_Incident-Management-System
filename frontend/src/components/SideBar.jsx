import { NavLink } from 'react-router-dom';
import './SideBar.css';

function SideBar({ newIncidents = [] }) {
  return (
    <aside className="dashboard-sidebar">
      <div className="sidebar-brand">
        <div className="sidebar-brand-mark">{'\u26A1'}</div>
        <div className="sidebar-brand-copy">
          <span className="sidebar-brand-title">IncidentIQ</span>
        </div>
      </div>

      <nav className="sidebar-nav" aria-label="Primary navigation">
        <NavLink
          to="/"
          end
          className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}
        >
          <span className="sidebar-link-icon">{'\u25C8'}</span>
          <span className="sidebar-link-label">Dashboard</span>
          {newIncidents.length > 0 && (
            <span className="sidebar-count">{newIncidents.length}</span>
          )}
        </NavLink>

        <NavLink
          to="/reports"
          className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}
        >
          <span className="sidebar-link-icon">{'\u25A4'}</span>
          <span className="sidebar-link-label">Reports</span>
        </NavLink>
      </nav>

      <div className="sidebar-spacer"></div>

      <div className="sidebar-profile">
        <div className="sidebar-avatar">YO</div>
        <div className="sidebar-profile-copy">
          <span className="sidebar-profile-name">You</span>
          <span className="sidebar-profile-role">SRE Engineer</span>
        </div>
      </div>
    </aside>
  );
}

export default SideBar;
