import { Link, useParams } from "react-router-dom";
import { jobs } from "../../data/mockData";

export default function JobDetail() {
  const { jobId } = useParams();
  const job = jobs.find(item => item.id === jobId) ?? jobs[0];

  return (
    <div className="page">
      <Link to="/student/jobs" className="back-link">← Back to jobs</Link>
      <div className="card detail-hero">
        <div><span className="badge">{job.match}% profile match</span><h1>{job.title}</h1><p>{job.company} · {job.location}</p></div>
        <div className="job-company-logo large">{job.company.charAt(0)}</div>
      </div>
      <div className="detail-grid">
        <section className="card">
          <span className="eyebrow">ROLE SKILLS</span>
          <h2>Skills relevant to this role</h2>
          <div className="skill-chips large-chips">{job.skills.map(skill => <span key={skill}>{skill}</span>)}</div>
          <h2>Readiness</h2>
          <p>Your readiness is calculated from your current skill evidence in this prototype. The production system will also validate evidence and labour-market data.</p>
        </section>
        <aside className="card">
          <span className="eyebrow">NEXT STEP</span>
          <h3>Improve your match</h3>
          <p>Review your skill gaps before applying so you can strengthen the most relevant evidence.</p>
          <Link to="/student/skill-gap" className="primary-button full">Review skill gaps</Link>
        </aside>
      </div>
    </div>
  );
}