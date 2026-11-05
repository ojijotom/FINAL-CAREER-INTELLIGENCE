import { Navigate, Outlet } from "react-router-dom";
import { roleHome, useAuth, type UserRole } from "./AuthContext";

export default function ProtectedRoute({ allowedRole }: { allowedRole: UserRole }) {
  const { user } = useAuth();

  if (!user) return <Navigate to="/login" replace />;
  if (user.role !== allowedRole) return <Navigate to={roleHome(user.role)} replace />;

  return <Outlet />;
}
