import { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth, roleHome, type UserRole } from "../../auth/AuthContext";
import { registerAccount } from "../../api";

const roleOptions: {
  value: UserRole;
  title: string;
  description: string;
  icon: string;
}[] = [
  {
    value: "student",
    title: "Student",
    description: "Discover careers, identify skill gaps and build employable skills.",
    icon: "🎓",
  },
  {
    value: "employer",
    title: "Employer",
    description: "Post jobs, discover talent and match candidates by skills.",
    icon: "🏢",
  },
  {
    value: "university",
    title: "University / Career Adviser",
    description: "Support students and monitor employability outcomes.",
    icon: "🏫",
  },
];

export default function Register() {
  const navigate = useNavigate();
  const { signIn } = useAuth();

  const [role, setRole] = useState<UserRole>("student");
  const [username, setUsername] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [institution, setInstitution] = useState("");
  const [programme, setProgramme] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");

    if (password !== confirmPassword) {
      setError("The passwords do not match.");
      return;
    }

    setLoading(true);

    const payload: Record<string, string> = {
      username: username.trim(),
      first_name: firstName.trim(),
      last_name: lastName.trim(),
      email: email.trim(),
      password,
      password_confirm: confirmPassword,
      role,
    };

    if (phoneNumber.trim()) {
      payload.phone_number = phoneNumber.trim();
    }

    if (role === "student") {
      payload.programme = programme.trim();
    } else if (role === "employer") {
      payload.company_name = institution.trim();
    } else {
      payload.institution_name = institution.trim();
    }

    try {
      const result = await registerAccount(payload);
      const profile = result.user;

      const fullName =
        `${profile.first_name} ${profile.last_name}`.trim() ||
        profile.username;

      signIn(
        {
          id: profile.id,
          username: profile.username,
          name: fullName,
          email: profile.email,
          role: profile.role,
          organisation: role === "student" ? undefined : institution.trim(),
          phone_number: profile.phone_number,
        },
        result.tokens,
      );

      navigate(roleHome(profile.role), { replace: true });
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Registration failed. Please check your details and try again.",
      );
    } finally {
      setLoading(false);
    }
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
            onClick={() => {
              setRole(option.value);
              setError("");
            }}
          >
            <span className="role-icon">{option.icon}</span>
            <strong>{option.title}</strong>
            <span>{option.description}</span>
          </button>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="form">
        <div className="two-inputs">
          <label>
            First name
            <input
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              placeholder="Alex"
              required
            />
          </label>

          <label>
            Last name
            <input
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              placeholder="Student"
              required
            />
          </label>
        </div>

        <label>
          Username
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Choose a username"
            autoComplete="username"
            required
          />
        </label>

        <label>
          Email address
          <input
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            type="email"
            placeholder="you@example.com"
            autoComplete="email"
            required
          />
        </label>

        <label>
          Phone number (optional)
          <input
            value={phoneNumber}
            onChange={(e) => setPhoneNumber(e.target.value)}
            type="tel"
            placeholder="0712345678"
          />
        </label>

        {role === "student" && (
          <label>
            Programme
            <input
              value={programme}
              onChange={(e) => setProgramme(e.target.value)}
              placeholder="BSc Computer Science"
              required
            />
          </label>
        )}

        {role === "employer" && (
          <label>
            Company / Organisation
            <input
              value={institution}
              onChange={(e) => setInstitution(e.target.value)}
              placeholder="Your company"
              required
            />
          </label>
        )}

        {role === "university" && (
          <label>
            University / Institution
            <input
              value={institution}
              onChange={(e) => setInstitution(e.target.value)}
              placeholder="Your university"
              required
            />
          </label>
        )}

        <label>
          Password
          <input
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            type="password"
            placeholder="Create a password"
            autoComplete="new-password"
            minLength={8}
            required
          />
        </label>

        <label>
          Confirm password
          <input
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            type="password"
            placeholder="Enter your password again"
            autoComplete="new-password"
            minLength={8}
            required
          />
        </label>

        {error && <div className="auth-error">{error}</div>}

        <button
          className="primary-button full"
          type="submit"
          disabled={loading}
        >
          {loading
            ? "Creating account..."
            : `Create ${roleOptions.find((r) => r.value === role)?.title} account`}
        </button>
      </form>

      <p className="auth-switch">
        Already have an account? <Link to="/login">Sign in</Link>
      </p>
    </section>
  );
}
