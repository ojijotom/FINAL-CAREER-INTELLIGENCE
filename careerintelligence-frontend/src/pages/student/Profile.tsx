import { useEffect, useState, type FormEvent } from "react";
import {
  getStudentProfile,
  updateStudentProfile,
  type StudentProfileData,
} from "../../api";
import { useAuth } from "../../auth/AuthContext";

export default function Profile() {
  const { user, accessToken } = useAuth();

  const [profile, setProfile] = useState<StudentProfileData | null>(null);
  const [educationLevel, setEducationLevel] = useState("");
  const [programme, setProgramme] = useState("");
  const [graduationYear, setGraduationYear] = useState("");
  const [experienceYears, setExperienceYears] = useState("");
  const [interests, setInterests] = useState("");
  const [location, setLocation] = useState("");
  const [bio, setBio] = useState("");

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    let active = true;

    async function loadProfile() {
      if (!accessToken) {
        setError("You are not logged in. Please sign in again.");
        setLoading(false);
        return;
      }

      try {
        const data = await getStudentProfile(accessToken);

        if (!active) return;

        setProfile(data);
        setEducationLevel(data.education_level || "");
        setProgramme(data.programme || "");
        setGraduationYear(
          data.graduation_year === null ? "" : String(data.graduation_year),
        );
        setExperienceYears(data.experience_years || "");
        setInterests((data.interests || []).join(", "));
        setLocation(data.location || "");
        setBio(data.bio || "");
        setError("");
      } catch (err) {
        if (active) {
          setError(
            err instanceof Error ? err.message : "Could not load your profile.",
          );
        }
      } finally {
        if (active) setLoading(false);
      }
    }

    loadProfile();

    return () => {
      active = false;
    };
  }, [accessToken]);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!accessToken) {
      setError("Your session has expired. Please sign in again.");
      return;
    }

    setSaving(true);
    setSaved(false);
    setError("");

    try {
      const result = await updateStudentProfile(accessToken, {
        programme,
        education_level: educationLevel,
        graduation_year: graduationYear
          ? Number(graduationYear)
          : null,
        experience_years: experienceYears || null,
        interests: interests
          .split(",")
          .map((item) => item.trim())
          .filter(Boolean),
        location,
        bio,
      });

      setProfile(result.profile);
      setSaved(true);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Could not save your profile.",
      );
    } finally {
      setSaving(false);
    }
  };

  const initials = (user?.name || "Student")
    .split(" ")
    .filter(Boolean)
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();

  return (
    <div className="page narrow-page">
      <div className="page-header">
        <div>
          <span className="eyebrow">STUDENT PROFILE</span>
          <h1>Your profile</h1>
          <p>Keep the information used by the career intelligence engine up to date.</p>
        </div>
      </div>

      {loading && <div className="card">Loading your profile...</div>}

      {error && <div className="error-message">{error}</div>}

      {saved && (
        <div className="success-message">
          Profile saved successfully to your account.
        </div>
      )}

      {!loading && profile && (
        <form className="card form profile-form" onSubmit={handleSubmit}>
          <div className="profile-avatar">{initials}</div>

          <div className="two-inputs">
            <label>
              First and last name
              <input value={user?.name || ""} readOnly />
            </label>
            <label>
              Email
              <input type="email" value={user?.email || ""} readOnly />
            </label>
          </div>

          <label>
            University
            <input
              value={
                profile.university === null
                  ? "Not linked to a university"
                  : `University record #${profile.university}`
              }
              readOnly
            />
          </label>

          <label>
            Programme
            <input
              value={programme}
              onChange={(event) => setProgramme(event.target.value)}
              placeholder="e.g. Computer Science"
            />
          </label>

          <label>
            Education level
            <input
              value={educationLevel}
              onChange={(event) => setEducationLevel(event.target.value)}
              placeholder="e.g. Undergraduate"
            />
          </label>

          <div className="two-inputs">
            <label>
              Expected graduation year
              <input
                type="number"
                min="2000"
                max="2100"
                value={graduationYear}
                onChange={(event) => setGraduationYear(event.target.value)}
                placeholder="e.g. 2028"
              />
            </label>

            <label>
              Years of experience
              <input
                type="number"
                min="0"
                step="0.1"
                value={experienceYears}
                onChange={(event) => setExperienceYears(event.target.value)}
                placeholder="e.g. 1.5"
              />
            </label>
          </div>

          <label>
            Career interests
            <input
              value={interests}
              onChange={(event) => setInterests(event.target.value)}
              placeholder="e.g. Software development, Data science"
            />
          </label>

          <label>
            Location
            <input
              value={location}
              onChange={(event) => setLocation(event.target.value)}
              placeholder="e.g. Kisii, Kenya"
            />
          </label>

          <label>
            About you
            <textarea
              value={bio}
              onChange={(event) => setBio(event.target.value)}
              rows={4}
              placeholder="Tell us about your background and career goals..."
            />
          </label>

          <button className="primary-button" type="submit" disabled={saving}>
            {saving ? "Saving..." : "Save profile"}
          </button>
        </form>
      )}
    </div>
  );
}
