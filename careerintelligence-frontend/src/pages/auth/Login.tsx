import { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth, roleHome, type UserRole } from "../../auth/AuthContext";

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

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");

    const saved = localStorage.getItem("career_intelligence_user");
    const existing = saved ? JSON.parse(saved) as { email: string; role: UserRole; name: string; organisation?: string } : null;

    // Prototype authentication. FastAPI will replace this later.
    if (existing && existing.email.toLowerCase() === email.toLowerCase()) {
      if (existing.role !== role) {
        setError(`This account is registered as ${roleLabels[existing.role]}. Select the correct account type.`);
        return;
      }
      signIn(existing);
      navigate(roleHome(existing.role), { replace: true });
      return;
    }

    // Demo fallback so the UI can be tested before the backend exists.
    const name = email.split("@")[0] || "Career Intelligence User";
    const user = { name, email, role };
    signIn(user);
    navigate(roleHome(role), { replace: true });
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
          <select value={role} onChange={(e) => setRole(e.target.value as UserRole)}>
            <option value="student">Student</option>
            <option value="employer">Employer</option>
            <option value="university">University / Career Adviser</option>
          </select>
        </label>
        <label>Email address<input value={email} onChange={(e) => setEmail(e.target.value)} type="email" placeholder="you@example.com" required /></label>
        <label>Password<input value={password} onChange={(e) => setPassword(e.target.value)} type="password" placeholder="••••••••" required /></label>
        {error && <div className="auth-error">{error}</div>}
        <button className="primary-button full" type="submit">Sign in</button>
      </form>

      <p className="auth-switch">Don't have an account? <Link to="/register">Create one</Link></p>
    </section>
  );
}
