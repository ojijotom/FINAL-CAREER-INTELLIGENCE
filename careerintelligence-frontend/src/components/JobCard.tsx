import { Link } from "react-router-dom";
import type { Job } from "../types";

export default function JobCard({ job }: { job: Job }) {
  return (
    <article className="card job-card">
      <div className="job-company-logo">{job.company.charAt(0)}</div>
      <div className="job-main">
        <div className="job-header">
          <div>
            <h3>{job.title}</h3>
            <p>{job.company} · {job.location}</p>
          </div>
          <span className="match">{job.match}% match</span>
        </div>
        <div className="skill-chips">
          {job.skills.map((skill) => <span key={skill}>{skill}</span>)}
        </div>
        <Link to={`/jobs/${job.id}`} className="text-link">View opportunity →</Link>
      </div>
    </article>
  );
}