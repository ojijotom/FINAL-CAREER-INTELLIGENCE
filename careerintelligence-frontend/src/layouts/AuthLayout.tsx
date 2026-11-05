import { Outlet } from "react-router-dom";
import Navbar from "../components/Navbar";

export default function AuthLayout() {
  return (
    <div className="auth-shell">
      <Navbar />
      <main className="auth-main">
        <Outlet />
      </main>
    </div>
  );
}