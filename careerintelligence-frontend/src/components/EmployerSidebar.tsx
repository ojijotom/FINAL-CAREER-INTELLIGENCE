import { Link, NavLink } from "react-router-dom";

const links = [
  { to: "/employer/dashboard", label: "Dashboard", icon: "⌂" },
  { to: "/employer/company", label: "Company Profile", icon: "▣" },
  { to: "/employer/post-job", label: "Post a Job", icon: "+" },
  { to: "/employer/jobs", label: "My Jobs", icon: "▤" },
  { to: "/employer/candidates", label: "Candidates", icon: "◎" },
  { to: "/employer/applications", label: "Applications", icon: "✓" },
  { to: "/employer/talent-search", label: "Talent Search", icon: "⌕" },
  { to: "/employer/settings", label: "Settings", icon: "⚙" },
];

export default function EmployerSidebar() {
  return (
    <aside className="employer-sidebar">
      <Link to="/employer/dashboard" className="employer-brand">
        <span className="brand-mark">CI</span>
        <span>Career Intelligence</span>
      </Link>

      <div className="portal-label">EMPLOYER PORTAL</div>

      <nav className="employer-nav" aria-label="Employer navigation">
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            className={({ isActive }) =>
              isActive ? "employer-nav-link active" : "employer-nav-link"
            }
          >
            <span className="nav-icon">{link.icon}</span>
            <span>{link.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-help">
        <div className="help-icon">?</div>
        <div>
          <strong>Need help?</strong>
          <span>Contact support</span>
        </div>
      </div>

      <div className="employer-account">
        <div className="company-avatar">TS</div>
        <div>
          <strong>Tech Solutions Ltd.</strong>
          <span>Employer</span>
        </div>
      </div>
    </aside>
  );
}