import {
  createContext,
  useContext,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import type { AuthTokens } from "../api";

export type UserRole = "student" | "employer" | "university";

export interface CurrentUser {
  id?: number;
  username?: string;
  name: string;
  email: string;
  role: UserRole;
  organisation?: string;
  phone_number?: string | null;
}

interface AuthContextValue {
  user: CurrentUser | null;
  accessToken: string | null;
  refreshToken: string | null;
  signIn: (user: CurrentUser, tokens: AuthTokens) => void;
  signOut: () => void;
}

const STORAGE_KEY = "career_intelligence_user";
const ACCESS_TOKEN_KEY = "career_intelligence_access";
const REFRESH_TOKEN_KEY = "career_intelligence_refresh";

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

function readStoredUser(): CurrentUser | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? (JSON.parse(raw) as CurrentUser) : null;
  } catch {
    return null;
  }
}

function readStoredToken(key: string): string | null {
  try {
    return localStorage.getItem(key);
  } catch {
    return null;
  }
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<CurrentUser | null>(readStoredUser);
  const [accessToken, setAccessToken] = useState<string | null>(
    () => readStoredToken(ACCESS_TOKEN_KEY),
  );
  const [refreshToken, setRefreshToken] = useState<string | null>(
    () => readStoredToken(REFRESH_TOKEN_KEY),
  );

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      accessToken,
      refreshToken,

      signIn(nextUser, tokens) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(nextUser));
        localStorage.setItem(ACCESS_TOKEN_KEY, tokens.access);
        localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh);

        setUser(nextUser);
        setAccessToken(tokens.access);
        setRefreshToken(tokens.refresh);
      },

      signOut() {
        localStorage.removeItem(STORAGE_KEY);
        localStorage.removeItem(ACCESS_TOKEN_KEY);
        localStorage.removeItem(REFRESH_TOKEN_KEY);

        setUser(null);
        setAccessToken(null);
        setRefreshToken(null);
      },
    }),
    [user, accessToken, refreshToken],
  );

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }

  return context;
}

export function roleHome(role: UserRole) {
  if (role === "student") return "/student/dashboard";
  if (role === "employer") return "/employer/dashboard";
  return "/university/dashboard";
}
