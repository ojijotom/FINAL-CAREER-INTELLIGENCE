
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  getStudentDashboard,
  type StudentDashboardData,
} from "../../api";
import { useAuth } from "../../auth/AuthContext";

export default function Dashboard() {
  const { user, accessToken } = useAuth();

  const [data, setData] = useState<StudentDashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!accessToken) {
      setError("Please log in to view your dashboard.");
      setLoading(false);
      return;
    }

    let cancelled = false;

    async function loadDashboard() {
      try {
        const dashboard = await getStudentDashboard(accessToken!);

        if (!cancelled) {
          setData(dashboard);
          setError("");
        }
      } catch (err) {
        if (!cancelled) {
          setError(
            err instanceof Error
              ? err.message
              : "Failed to load dashboard data.",
          );
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    loadDashboard();

    return () => {
      cancelled = true;
    };
  }, [accessToken]);

  const studentName =
    data?.student.first_name?.trim() ||
    user?.name?.trim() ||
    user?.username ||
    "Student";

  if (loading) {
    return (
      <div className="page">
        <div className="page-header">
          <div>
            <span className="eyebrow">STUDENT DASHBOARD</span>
            <h1>Loading your dashboard...</h1>
            <p>Retrieving your information from the database.</p>
          </div>
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="page">
        <div className="page-header">
          <div>
            <span className="eyebrow">STUDENT DASHBOARD</span>
            <h1>Hello, {studentName.split(" ")[0]}</h1>
            <p>Your dashboard could not retrieve your information.</p>
          </div>
          <Link to="/student/profile" className="secondary-button">
            Update profile
          </Link>
        </div>

        <div className="card">
          <p>{error || "No dashboard data was returned."}</p>
          <button
            className="secondary-button"
            onClick={() => window.location.reload()}
          >
            Try again
          </button>
        </div>
      </div>
    );
  }

  const { statistics, skills, vacancies, applications, career_analyses } =
    data;

  const latestCareerAnalysis = career_analyses.find(
    (item) => item.analysis_type === "career_match",
  );

  const formatSource = (source: string) =>
    source.replaceAll("_", " ").replace(/\b\w/g, (letter) =>
      letter.toUpperCase(),
    );

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <span className="eyebrow">STUDENT DASHBOARD</span>
          <h1>Hello, {studentName.split(" ")[0]}</h1>
          <p>
            {data.student.programme || "Your career intelligence overview"}
          </p>
        </div>
        <Link to="/student/profile" className="secondary-button">
          Update profile
        </Link>
      </div>

      <section className="dashboard-grid">
        <div className="stat-card highlight">
          <span>Career compatibility</span>
          <strong>
            {latestCareerAnalysis ? "Available" : "--"}
          </strong>
          <small>
            {latestCareerAnalysis
              ? `Last analysis: ${new Date(
                  latestCareerAnalysis.created_at,
                ).toLocaleDateString()}`
              : "Generate your career analysis"}
          </small>
        </div>

        <div className="stat-card">
          <span>Average skill level</span>
          <strong>
            {statistics.average_skill_level !== null
              ? `${statistics.average_skill_level}%`
              : "--"}
          </strong>
          <small>
            {statistics.assessed_skills_count} assessed out of{" "}
            {statistics.skills_count} skills
          </small>
        </div>

        <div className="stat-card">
          <span>Documents uploaded</span>
          <strong>{statistics.documents_count}</strong>
          <small>
            {statistics.verified_documents_count} verified documents
          </small>
        </div>

        <div className="stat-card">
          <span>Active vacancies</span>
          <strong>{statistics.active_vacancies_count}</strong>
          <small>{statistics.applications_count} applications submitted</small>
        </div>
      </section>

      <section>
        <div className="section-heading compact">
          <div>
            <span className="eyebrow">YOUR SKILLS</span>
            <h2>Skills detected and recorded</h2>
          </div>
          <Link to="/student/skills" className="text-link">
            Manage skills
          </Link>
        </div>

        {skills.length === 0 ? (
          <div className="card">
            <p>
              No skills have been recorded yet. Upload your CV to allow the
              system to identify skills from its contents.
            </p>
            <Link to="/student/cv-upload" className="primary-button">
              Upload CV
            </Link>
          </div>
        ) : (
          <div className="card">
            <div className="skills-list">
              {skills.map((skill) => (
                <div className="skill-item" key={skill.id}>
                  <div>
                    <strong>{skill.name}</strong>
                    <small>
                      {skill.category} · {formatSource(skill.source)}
                      {skill.verified ? " · Verified" : " · Not verified"}
                    </small>
                    {skill.evidence_description && (
                      <p>{skill.evidence_description}</p>
                    )}
                  </div>
                  <span>
                    {skill.level !== null ? `${skill.level}%` : "Not assessed"}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </section>

      <section className="dashboard-columns">
        <div>
          <div className="section-heading compact">
            <div>
              <span className="eyebrow">CAREER DIRECTION</span>
              <h2>Career analyses</h2>
            </div>
            <Link to="/student/careers" className="text-link">
              View careers
            </Link>
          </div>

          {career_analyses.length === 0 ? (
            <div className="card">
              <p>
                Your completed career analyses will appear here.
              </p>
              <Link to="/student/careers" className="text-link">
                Explore careers
              </Link>
            </div>
          ) : (
            <div className="card">
              {career_analyses.map((analysis) => (
                <div className="skill-item" key={analysis.id}>
                  <div>
                    <strong>
                      {analysis.career || analysis.analysis_type.replaceAll("_", " ")}
                    </strong>
                    <small>
                      {analysis.analysis_type.replaceAll("_", " ")} ·{" "}
                      {new Date(analysis.created_at).toLocaleDateString()}
                    </small>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <aside className="card next-action">
          <span className="eyebrow">NEXT BEST ACTION</span>
          <div className="action-icon">✦</div>
          <h3>Strengthen your career profile</h3>
          <p>
            Upload your CV and transcript, review detected skills and complete
            your profile to improve your career intelligence results.
          </p>
          <Link to="/student/profile" className="primary-button full">
            Complete profile
          </Link>
        </aside>
      </section>

      <section>
        <div className="section-heading compact">
          <div>
            <span className="eyebrow">OPPORTUNITIES</span>
            <h2>Available vacancies</h2>
          </div>
          <Link to="/student/jobs" className="text-link">
            View all jobs
          </Link>
        </div>

        {vacancies.length === 0 ? (
          <div className="card">
            <p>There are currently no active vacancies available.</p>
          </div>
        ) : (
          <div className="card">
            {vacancies.map((vacancy) => (
              <div className="skill-item" key={vacancy.id}>
                <div>
                  <strong>{vacancy.title}</strong>
                  <small>
                    {vacancy.company} · {vacancy.location} ·{" "}
                    {vacancy.employment_type} · {vacancy.work_mode}
                  </small>
                  {vacancy.closing_date && (
                    <small>
                      Closing:{" "}
                      {new Date(vacancy.closing_date).toLocaleDateString()}
                    </small>
                  )}
                </div>
                <Link to="/student/jobs" className="text-link">
                  View
                </Link>
              </div>
            ))}
          </div>
        )}
      </section>

      <section>
        <div className="section-heading compact">
          <div>
            <span className="eyebrow">APPLICATION ACTIVITY</span>
            <h2>Recent applications</h2>
          </div>
        </div>

        {applications.length === 0 ? (
          <div className="card">
            <p>You have not submitted any job applications yet.</p>
          </div>
        ) : (
          <div className="card">
            {applications.map((application) => (
              <div className="skill-item" key={application.id}>
                <div>
                  <strong>{application.job_title}</strong>
                  <small>
                    {application.company} ·{" "}
                    {new Date(application.applied_at).toLocaleDateString()}
                  </small>
                </div>
                <span>{application.status.replaceAll("_", " ")}</span>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
