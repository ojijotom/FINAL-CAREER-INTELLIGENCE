const applications = [
  ["Alex Student", "Data Analyst", "Shortlisted", "92%"],
  ["Brian Otieno", "Software Developer", "Under Review", "88%"],
  ["Mary Wanjiku", "Network Engineer", "Interview", "84%"],
  ["Kevin Mwangi", "Data Analyst", "Applied", "81%"],
];

export default function Applications() {
  return (
    <div className="page">
      <div className="page-heading">
        <div><span className="eyebrow">RECRUITMENT PIPELINE</span><h1>Applications</h1><p>Track candidates through your recruitment process.</p></div>
      </div>
      <section className="panel">
        <div className="pipeline">
          {applications.map(([name, role, status, match]) => (
            <div className="application-row" key={`${name}-${role}`}>
              <div className="candidate-avatar small">{name.split(" ").map(p => p[0]).join("")}</div>
              <div className="application-main"><strong>{name}</strong><span>{role}</span></div>
              <span className={`status ${status === "Interview" || status === "Shortlisted" ? "active-status" : "draft-status"}`}>{status}</span>
              <strong className="application-match">{match}</strong>
              <button className="table-action">Review</button>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}