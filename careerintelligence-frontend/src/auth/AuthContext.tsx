import { createContext, useContext, useMemo, useState, type ReactNode } from "react";

export type UserRole = "student" | "employer" | "university";

export interface CurrentUser {
  name: string;
  email: string;
  role: UserRole;
  organisation?: string;
}

interface AuthContextValue {
  user: CurrentUser | null;
  signIn: (user: CurrentUser) => void;
  signOut: () => void;
}

const STORAGE_KEY = "career_intelligence_user";

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

function readStoredUser(): CurrentUser | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<CurrentUser | null>(readStoredUser);

  const value = useMemo<AuthContextValue>(() => ({
    user,
    signIn(nextUser) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(nextUser));
      setUser(nextUser);
    },
    signOut() {
      localStorage.removeItem(STORAGE_KEY);
      setUser(null);
    },
  }), [user]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used inside AuthProvider");
  return context;
}

export function roleHome(role: UserRole) {
  if (role === "student") return "/student/dashboard";
  if (role === "employer") return "/employer/dashboard";
  return "/university/dashboard";
}
