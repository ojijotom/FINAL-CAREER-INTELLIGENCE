import { Link } from "react-router-dom";

export default function UniversityDashboard() {
  return (
    <div className="page university-dashboard">
      <div className="page-header">
        <div>
          <span className="eyebrow">UNIVERSITY / CAREER ADVISER</span>
          <h1>Career Services Dashboard</h1>
          <p>Monitor student employability, skill gaps and career readiness.</p>
        </div>
        <Link className="primary-button" to="/student/dashboard">Preview Student Portal</Link>
      </div>

      <div className="dashboard-grid">
        <div className="stat-card"><span>Students tracked</span><strong>1,248</strong><small>Across active programmes</small></div>
        <div className="stat-card"><span>Career readiness</span><strong>74%</strong><small>Average readiness score</small></div>
        <div className="stat-card"><span>Top skill gap</span><strong>Power BI</strong><small>Most common intervention</small></div>
        <div className="stat-card"><span>Employer links</span><strong>86</strong><small>Active employer partners</small></div>
      </div>

      <div className="cards-grid two">
        <section className="card">
          <span className="eyebrow">STUDENT INSIGHTS</span>
          <h3>Skills-gap intelligence</h3>
          <p>Identify skills that students most frequently need to develop for their target careers and employer demand.</p>
        </section>
        <section className="card">
          <span className="eyebrow">CURRICULUM INTELLIGENCE</span>
          <h3>Industry alignment</h3>
          <p>Compare programme outcomes with labour-market requirements to support evidence-based curriculum improvement.</p>
        </section>
      </div>
    </div>
  );
}
