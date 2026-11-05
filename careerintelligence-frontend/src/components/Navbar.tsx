import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <header className="topbar">
      <Link to="/" className="brand">
        <span className="brand-mark">CI</span>
        <span>Career Intelligence</span>
      </Link>
      <nav className="topnav">
        <Link to="/">Home</Link>
        <Link to="/register" className="nav-button">Get started</Link>
        <Link to="/login" className="nav-button">Sign in</Link>
      </nav>
    </header>
  );
}
