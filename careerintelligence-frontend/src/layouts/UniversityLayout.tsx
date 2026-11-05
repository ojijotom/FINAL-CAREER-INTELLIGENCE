import { Outlet } from "react-router-dom";
import { Link, NavLink } from "react-router-dom";

const links = [
  { to: "/university/dashboard", label: "Dashboard", icon: "⌂" },
];

export default function UniversityLayout() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <Link to="/university/dashboard" className="brand sidebar-brand">
          <span className="brand-mark">CI</span>
          <span>Career Intelligence</span>
        </Link>
        <div className="sidebar-section-title">UNIVERSITY PORTAL</div>
        <nav className="sidebar-nav">
          {links.map((link) => (
            <NavLink key={link.to} to={link.to} className={({isActive}) => isActive ? "side-link active" : "side-link"}>
              <span className="side-icon">{link.icon}</span><span>{link.label}</span>
            </NavLink>
          ))}
        </nav>
        <div className="sidebar-footer">
          <div className="mini-profile"><div className="avatar">CA</div><div><strong>Career Adviser</strong><span>University</span></div></div>
        </div>
      </aside>
      <main className="content"><Outlet /></main>
    </div>
  );
}
