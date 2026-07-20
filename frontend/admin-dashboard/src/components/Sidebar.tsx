import { NavLink } from 'react-router-dom';
import { ShieldCheck, Ticket, LogOut } from 'lucide-react';

const Sidebar = () => {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <ShieldCheck size={24} color="var(--primary)" />
        <span>Admin Portal</span>
      </div>
      
      <nav className="sidebar-nav">
        <NavLink 
          to="/approvals" 
          className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
        >
          <ShieldCheck size={18} />
          Pending Approvals
        </NavLink>
        
        <NavLink 
          to="/tickets" 
          className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
        >
          <Ticket size={18} />
          Support Tickets
        </NavLink>
      </nav>
      
      <div style={{ padding: '1.5rem', borderTop: '1px solid var(--panel-border)' }}>
        <button 
          className="nav-item" 
          style={{ width: '100%', background: 'transparent', border: 'none', cursor: 'pointer' }}
          onClick={() => alert("Logged out")}
        >
          <LogOut size={18} />
          Sign Out
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
