import { NavLink } from "react-router-dom";
import { Link } from "react-router-dom";
const links = [
  { to: "/student/dashboard", label: "Dashboard", icon: "⌂" },
  { to: "/student/careers", label: "Careers", icon: "◎" },
  { to: "/student/skills", label: "Skills", icon: "◆" },
  { to: "/student/skill-gap", label: "Skill Gap", icon: "△" },
  { to: "/student/jobs", label: "Jobs", icon: "▣" },
  { to: "/student/profile", label: "Profile", icon: "●" },
  { to: "/student/evidence", label: "My Evidence", icon: "📄" },
  { to: "/student/settings", label: "Settings", icon: "⚙" },

    
    
    
  
];

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <Link to="/" className="brand sidebar-brand">
        <span className="brand-mark">CI</span>
        <span>Career Intelligence</span>
      </Link>

      <div className="sidebar-section-title">MAIN MENU</div>

      <nav className="sidebar-nav">
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            className={({ isActive }) => isActive ? "side-link active" : "side-link"}
          >
            <span className="side-icon">{link.icon}</span>
            <span>{link.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div className="mini-profile">
          <div className="avatar">AS</div>
          <div>
            <strong>Alex Student</strong>
            <span>Student</span>
          </div>
        </div>
      </div>
    </aside>
  );
}