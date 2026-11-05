import { Link } from "react-router-dom";

const candidates = [
  ["Alex Student", "Data Analyst", "92%", "Power BI"],
  ["Brian Otieno", "Software Developer", "88%", "Testing"],
  ["Mary Wanjiku", "Network Engineer", "84%", "Cloud Security"],
  ["Kevin Mwangi", "Data Analyst", "81%", "Statistics"],
];

export default function Candidates() {
  return (
    <div className="page">
      <div className="page-heading">
        <div><span className="eyebrow">SKILLS-FIRST TALENT</span><h1>Candidates</h1><p>Review candidates ranked by compatibility and evidence.</p></div>
      </div>
      <div className="filter-bar">
        <input placeholder="Search candidates..." />
        <select defaultValue="all"><option value="all">All roles</option><option>Data Analyst</option><option>Software Developer</option><option>Network Engineer</option></select>
        <select defaultValue="match"><option value="match">Best match first</option><option>Newest first</option></select>
      </div>
      <section className="candidate-list">
        {candidates.map(([name, role, match, gap]) => (
          <Link className="candidate-list-card" to={`/employer/candidate/${name.toLowerCase().replaceAll(" ", "-")}`} key={name}>
            <div className="candidate-avatar">{name.split(" ").map(p => p[0]).join("")}</div>
            <div className="candidate-details"><strong>{name}</strong><span>{role}</span><small>Priority gap: {gap}</small></div>
            <div className="candidate-match"><strong>{match}</strong><span>match</span></div>
            <span className="secondary-button">View profile</span>
          </Link>
        ))}
      </section>
    </div>
  );
}