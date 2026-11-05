import { Outlet } from "react-router-dom";
import Sidebar from "../components/Sidebar";

export default function StudentLayout() {
  return (
    <div className="app-shell">
      <Sidebar />
      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}