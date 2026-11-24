
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  getStudentProfile,
  getStudentDocuments,
  type StudentProfileData,
  type StudentDocument,
} from "../../api";
import { useAuth } from "../../auth/AuthContext";
import CareerCard from "../../components/CareerCard";
import JobCard from "../../components/JobCard";
import ProgressBar from "../../components/ProgressBar";

interface DashboardData {
  profile: StudentProfileData | null;
  documents: StudentDocument[];
}

export default function Dashboard() {
  const { user, accessToken } = useAuth();

  const [data, setData] = useState<DashboardData>({
    profile: null,
    documents: [],
  });
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
        const [profile, documents] = await Promise.all([
          getStudentProfile(accessToken),
          getStudentDocuments(accessToken),
        ]);

        if (!cancelled) {
          setData({ profile, documents });
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
    user?.name?.trim() ||
    user?.username ||
    "Student";

  const evidenceCount = data.documents.length;

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

  if (error) {
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
          <p>{error}</p>
          <p>Please check your connection and try again.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <span className="eyebrow">STUDENT DASHBOARD</span>
          <h1>Good morning, {studentName.split(" ")[0]}</h1>
          <p>Here is your current career intelligence overview.</p>
        </div>
        <Link to="/student/profile" className="secondary-button">
          Update profile
        </Link>
      </div>

      <section className="dashboard-grid">
        <div className="stat-card highlight">
          <span>Career compatibility</span>
          <strong>--</strong>
          <small>Generate your career analysis</small>
        </div>

        <div className="stat-card">
          <span>Skill readiness</span>
          <strong>--</strong>
          <small>Based on assessed skills</small>
        </div>

        <div className="stat-card">
          <span>Evidence collected</span>
          <strong>{evidenceCount}</strong>
          <small>Documents uploaded to your profile</small>
        </div>

        <div className="stat-card">
          <span>Job matches</span>
          <strong>--</strong>
          <small>Real vacancies will appear here</small>
        </div>
      </section>

      <section className="dashboard-columns">
        <div>
          <div className="section-heading compact">
            <div>
              <span className="eyebrow">CAREER DIRECTION</span>
              <h2>Recommended careers</h2>
            </div>
            <Link to="/student/careers" className="text-link">
              View all
            </Link>
          </div>

          <div className="card">
            <p>Your career recommendations will appear after your career analysis is completed.</p>
            <Link to="/student/careers" className="text-link">
              Explore careers
            </Link>
          </div>
        </div>

        <aside className="card next-action">
          <span className="eyebrow">NEXT BEST ACTION</span>
          <div className="action-icon">✦</div>
          <h3>Complete your career profile</h3>
          <p>
            Add your education, skills and career interests to help generate
            meaningful career intelligence.
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
            <h2>Recommended jobs</h2>
          </div>
          <Link to="/student/jobs" className="text-link">
            View all
          </Link>
        </div>

        <div className="card">
          <p>Job recommendations will appear when real vacancies are available.</p>
          <Link to="/student/jobs" className="text-link">
            Explore jobs
          </Link>
        </div>
      </section>
    </div>
  );
}
