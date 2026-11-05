import { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth, roleHome, type UserRole } from "../../auth/AuthContext";

const roleOptions: { value: UserRole; title: string; description: string; icon: string }[] = [
  { value: "student", title: "Student", description: "Discover careers, identify skill gaps and build employable skills.", icon: "🎓" },
  { value: "employer", title: "Employer", description: "Post jobs, discover talent and match candidates by skills.", icon: "🏢" },
  { value: "university", title: "University / Career Adviser", description: "Support students and monitor employability outcomes.", icon: "🏫" },
];

export default function Register() {
  const navigate = useNavigate();
  const { signIn } = useAuth();
  const [role, setRole] = useState<UserRole>("student");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [institution, setInstitution] = useState("");
  const [programme, setProgramme] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const user = {
      name: `${firstName} ${lastName}`.trim(),
      email,
      role,
      organisation: institution,
    };

    signIn(user);
    navigate(roleHome(role), { replace: true });
  };

  return (
    <section className="auth-card register-card">
      <div className="auth-heading">
        <span className="eyebrow">CREATE YOUR ACCOUNT</span>
        <h1>Get started</h1>
        <p>Choose how you will use Career Intelligence.</p>
      </div>

      <div className="role-grid">
        {roleOptions.map((option) => (
          <button
            type="button"
            key={option.value}
            className={`role-card ${role === option.value ? "selected" : ""}`}
            onClick={() => setRole(option.value)}
          >
            <span className="role-icon">{option.icon}</span>
            <strong>{option.title}</strong>
            <span>{option.description}</span>
          </button>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="form">
        <div className="two-inputs">
          <label>First name<input value={firstName} onChange={(e) => setFirstName(e.target.value)} placeholder="Alex" required /></label>
          <label>Last name<input value={lastName} onChange={(e) => setLastName(e.target.value)} placeholder="Student" required /></label>
        </div>
        <label>Email address<input value={email} onChange={(e) => setEmail(e.target.value)} type="email" placeholder="you@example.com" required /></label>

        {role === "student" && (
          <>
            <label>University / Institution<input value={institution} onChange={(e) => setInstitution(e.target.value)} placeholder="Your university" required /></label>
            <label>Programme<input value={programme} onChange={(e) => setProgramme(e.target.value)} placeholder="BSc Information Technology" required /></label>
          </>
        )}

        {role === "employer" && (
          <>
            <label>Company / Organisation<input value={institution} onChange={(e) => setInstitution(e.target.value)} placeholder="Your company" required /></label>
            <label>Position<input value={programme} onChange={(e) => setProgramme(e.target.value)} placeholder="HR Manager / Recruiter" required /></label>
          </>
        )}

        {role === "university" && (
          <>
            <label>University / Institution<input value={institution} onChange={(e) => setInstitution(e.target.value)} placeholder="Your university" required /></label>
            <label>Department / Position<input value={programme} onChange={(e) => setProgramme(e.target.value)} placeholder="Career Services" required /></label>
          </>
        )}

        <label>Password<input value={password} onChange={(e) => setPassword(e.target.value)} type="password" placeholder="Create a password" minLength={8} required /></label>
        <button className="primary-button full" type="submit">Create {roleOptions.find((r) => r.value === role)?.title} account</button>
      </form>

      <p className="auth-switch">Already have an account? <Link to="/login">Sign in</Link></p>
    </section>
  );
}
