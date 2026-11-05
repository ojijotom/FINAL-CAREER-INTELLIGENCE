import { Link } from "react-router-dom";

export default function EmployerTopbar() {
  return (
    <header className="employer-topbar">
      <span className="topbar-kicker">EMPLOYER WORKSPACE</span>
      <div className="topbar-actions">
        <button className="icon-button" aria-label="Notifications">♧<span className="notification-dot" /></button>
        <Link className="view-public" to="/">View public site</Link>
        <div className="topbar-avatar">TS</div>
      </div>
    </header>
  );
}