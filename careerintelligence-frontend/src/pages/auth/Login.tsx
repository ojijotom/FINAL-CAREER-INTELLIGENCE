import { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth, roleHome, type UserRole } from "../../auth/AuthContext";
import { getCurrentUser, loginAccount } from "../../api";

const roleLabels: Record<UserRole, string> = {
  student: "Student",
  employer: "Employer",
  university: "University / Career Adviser",
};

export default function Login() {
  const navigate = useNavigate();
  const { signIn } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState<UserRole>("student");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      const tokens = await loginAccount(email.trim(), password);
      const profile = await getCurrentUser(tokens.access);

      if (profile.role !== role) {
        setError(
          `This account is registered as ${roleLabels[profile.role]}. Select the correct account type.`,
        );
        return;
      }

      const fullName =
        `${profile.first_name} ${profile.last_name}`.trim() ||
        profile.username;

      const user = {
        id: profile.id,
        username: profile.username,
        name: fullName,
        email: profile.email,
        role: profile.role,
        phone_number: profile.phone_number,
      };

      signIn(user, tokens);
      navigate(roleHome(profile.role), { replace: true });
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Login failed. Please check your details and try again.",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="auth-card">
      <div className="auth-heading">
        <span className="eyebrow">WELCOME BACK</span>
        <h1>Sign in</h1>
        <p>Continue your Career Intelligence journey.</p>
      </div>

      <form onSubmit={handleSubmit} className="form">
        <label>
          Account type
          <select
            value={role}
            onChange={(e) => setRole(e.target.value as UserRole)}
          >
            <option value="student">Student</option>
            <option value="employer">Employer</option>
            <option value="university">University / Career Adviser</option>
          </select>
        </label>

        <label>
          Email address or username
          <input
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            type="text"
            placeholder="Email or username"
            autoComplete="username"
            required
          />
        </label>

        <label>
          Password
          <input
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            type="password"
            placeholder="Enter your password"
            autoComplete="current-password"
            required
          />
        </label>

        {error && <div className="auth-error">{error}</div>}

        <button
          className="primary-button full"
          type="submit"
          disabled={loading}
        >
          {loading ? "Signing in..." : "Sign in"}
        </button>
      </form>

      <p className="auth-switch">
        Don't have an account? <Link to="/register">Create one</Link>
      </p>
    </section>
  );
}
