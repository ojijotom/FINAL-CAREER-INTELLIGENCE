import { Link } from "react-router-dom";
import { careers, jobs, skills, studentProfile } from "../../data/mockData";
import CareerCard from "../../components/CareerCard";
import JobCard from "../../components/JobCard";
import ProgressBar from "../../components/ProgressBar";

export default function Dashboard() {
  const biggestGap = [...skills].sort((a, b) => (b.target - b.level) - (a.target - a.level))[0];

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <span className="eyebrow">STUDENT DASHBOARD</span>
          <h1>Good morning, {studentProfile.name.split(" ")[0]}</h1>
          <p>Here is your current career intelligence overview.</p>
        </div>
        <Link to="/student/profile" className="secondary-button">Update profile</Link>
      </div>

      <section className="dashboard-grid">
        <div className="stat-card highlight"><span>Career compatibility</span><strong>78%</strong><small>Based on your current profile</small></div>
        <div className="stat-card"><span>Skill readiness</span><strong>68%</strong><small>Across your target skills</small></div>
        <div className="stat-card"><span>Evidence collected</span><strong>12</strong><small>Academic + practical evidence</small></div>
        <div className="stat-card"><span>Job matches</span><strong>18</strong><small>Current sample opportunities</small></div>
      </section>

      <section className="dashboard-columns">
        <div>
          <div className="section-heading compact"><div><span className="eyebrow">CAREER DIRECTION</span><h2>Recommended careers</h2></div><Link to="/student/careers" className="text-link">View all</Link></div>
          <div className="cards-grid">{careers.slice(0, 2).map(career => <CareerCard key={career.id} career={career} />)}</div>
        </div>

        <aside className="card next-action">
          <span className="eyebrow">NEXT BEST ACTION</span>
          <div className="action-icon">✦</div>
          <h3>Close your {biggestGap.name} gap</h3>
          <p>Your current level is {biggestGap.level}%, while the target for your selected career is {biggestGap.target}%.</p>
          <ProgressBar value={biggestGap.level} label="Current level" />
          <Link to="/student/skill-gap" className="primary-button full">View skill-gap plan</Link>
        </aside>
      </section>

      <section>
        <div className="section-heading compact"><div><span className="eyebrow">OPPORTUNITIES</span><h2>Recommended jobs</h2></div><Link to="/student/jobs" className="text-link">View all</Link></div>
        <div className="job-list">{jobs.slice(0, 2).map(job => <JobCard key={job.id} job={job} />)}</div>
      </section>
    </div>
  );
}