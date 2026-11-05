import { Link } from "react-router-dom";
import StatCard from "../../components/StatCard";

const jobs = [
  { title: "Data Analyst", applications: 24, status: "Active", skills: "SQL · Excel · Power BI" },
  { title: "Software Developer", applications: 31, status: "Active", skills: "React · Python · APIs" },
  { title: "Network Engineer", applications: 29, status: "Active", skills: "Networking · Linux · Security" },
];

const candidates = [
  { name: "Alex Student", role: "Data Analyst", match: 92, gap: "Power BI" },
  { name: "Brian Otieno", role: "Software Developer", match: 88, gap: "Testing" },
  { name: "Mary Wanjiku", role: "Network Engineer", match: 84, gap: "Cloud Security" },
];

export default function EmployerDashboard() {
  return (
    <div className="page">
      <div className="page-heading">
        <div>
          <span className="eyebrow">EMPLOYER DASHBOARD</span>
          <h1>Good morning, Tech Solutions.</h1>
          <p>Use skills intelligence to discover and evaluate the right talent.</p>
        </div>
        <Link className="primary-button" to="/employer/post-job">+ Post a Job</Link>
      </div>

      <section className="stats-grid">
        <StatCard label="Active Jobs" value="6" note="+2 this month" icon="▤" />
        <StatCard label="Applications" value="84" note="+18 this week" icon="✓" />
        <StatCard label="Shortlisted" value="18" note="21% of applicants" icon="★" />
        <StatCard label="Potential Matches" value="32" note="AI-ranked talent" icon="◎" />
      </section>

      <section className="dashboard-grid">
        <div className="panel large-panel">
          <div className="panel-heading">
            <div><h2>Recent Jobs</h2><p>Monitor your active opportunities.</p></div>
            <Link to="/employer/jobs">View all</Link>
          </div>
          <div className="job-list">
            {jobs.map((job) => (
              <div className="job-row" key={job.title}>
                <div className="job-symbol">▣</div>
                <div className="job-main"><strong>{job.title}</strong><span>{job.skills}</span></div>
                <div className="job-applications"><strong>{job.applications}</strong><span>applications</span></div>
                <span className="status active-status">{job.status}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="panel">
          <div className="panel-heading"><div><h2>Hiring Snapshot</h2><p>This month</p></div></div>
          <div className="snapshot">
            <div className="snapshot-number">78%</div>
            <div className="snapshot-title">Average candidate match</div>
            <p>Skills-first matching helps your team focus on relevant evidence.</p>
          </div>
          <div className="mini-metrics">
            <div><strong>42</strong><span>Reviewed</span></div>
            <div><strong>18</strong><span>Shortlisted</span></div>
            <div><strong>7</strong><span>Interviews</span></div>
          </div>
        </div>
      </section>

      <section className="panel">
        <div className="panel-heading">
          <div><h2>Recommended Talent</h2><p>Candidates ranked by skills, evidence and job requirements.</p></div>
          <Link to="/employer/candidates">View candidates</Link>
        </div>
        <div className="candidate-grid">
          {candidates.map((candidate) => (
            <Link
              className="candidate-card"
              to={`/employer/candidate/${candidate.name.toLowerCase().replaceAll(" ", "-")}`}
              key={candidate.name}
            >
              <div className="candidate-header">
                <div className="candidate-avatar">{candidate.name.split(" ").map((part) => part[0]).join("")}</div>
                <div><strong>{candidate.name}</strong><span>{candidate.role}</span></div>
                <div className="match-score">{candidate.match}%</div>
              </div>
              <div className="match-label">AI compatibility</div>
              <div className="match-bar"><span style={{ width: `${candidate.match}%` }} /></div>
              <div className="candidate-gap"><span>Priority gap</span><strong>{candidate.gap}</strong></div>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}