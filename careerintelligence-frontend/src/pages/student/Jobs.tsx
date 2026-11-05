import JobCard from "../../components/JobCard";
import { jobs } from "../../data/mockData";

export default function Jobs() {
  return (
    <div className="page">
      <div className="page-header"><div><span className="eyebrow">CAREER OPPORTUNITIES</span><h1>Job matches</h1><p>Opportunities aligned with your current skills and target career.</p></div></div>
      <div className="filter-bar"><input placeholder="Search jobs..." /><select defaultValue="all"><option value="all">All locations</option><option>Nairobi, Kenya</option><option>Hybrid</option></select></div>
      <div className="job-list">{jobs.map(job => <JobCard key={job.id} job={job} />)}</div>
    </div>
  );
}