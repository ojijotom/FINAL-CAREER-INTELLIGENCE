import { Outlet } from "react-router-dom";
import EmployerSidebar from "../components/EmployerSidebar";
import EmployerTopbar from "../components/EmployerTopbar";

export default function EmployerLayout() {
  return (
    <div className="employer-portal employer-app">
      <EmployerSidebar />
      <div className="employer-main">
        <EmployerTopbar />
        <main className="employer-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}