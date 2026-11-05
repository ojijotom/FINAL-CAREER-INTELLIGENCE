import { Link } from "react-router-dom";

const jobs = [
  ["Data Analyst", "24", "Active", "Nairobi"],
  ["Software Developer", "31", "Active", "Nairobi"],
  ["Network Engineer", "29", "Active", "Hybrid"],
  ["UI/UX Designer", "0", "Draft", "Nairobi"],
];

export default function MyJobs() {
  return (
    <div className="page">
      <div className="page-heading">
        <div><span className="eyebrow">JOB MANAGEMENT</span><h1>My Jobs</h1><p>Create, monitor and manage your recruitment opportunities.</p></div>
        <Link className="primary-button" to="/employer/post-job">+ Post a Job</Link>
      </div>
      <section className="panel">
        <div className="table-wrap">
          <table>
            <thead><tr><th>Job</th><th>Applications</th><th>Location</th><th>Status</th><th></th></tr></thead>
            <tbody>
              {jobs.map(([title, applications, status, location]) => (
                <tr key={title}>
                  <td><strong>{title}</strong></td><td>{applications}</td><td>{location}</td>
                  <td><span className={`status ${status === "Active" ? "active-status" : "draft-status"}`}>{status}</span></td>
                  <td><button className="table-action">Manage</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}