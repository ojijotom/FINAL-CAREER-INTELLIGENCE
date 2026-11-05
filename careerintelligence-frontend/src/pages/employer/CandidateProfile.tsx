import { Link, useParams } from "react-router-dom";

const skills = [
  ["SQL", 88], ["Excel", 94], ["Statistics", 80], ["Data Visualization", 76], ["Power BI", 55],
];

export default function CandidateProfile() {
  const { candidateId } = useParams();
  const name = (candidateId ?? "candidate").split("-").map(part => part.charAt(0).toUpperCase() + part.slice(1)).join(" ");

  return (
    <div className="page">
      <Link className="back-link" to="/employer/candidates">← Back to candidates</Link>

      <section className="candidate-profile-hero panel">
        <div className="large-candidate-avatar">AS</div>
        <div><span className="eyebrow">CANDIDATE PROFILE</span><h1>{name}</h1><p>Data Analyst · Student / Early Career</p></div>
        <div className="hero-match"><strong>92%</strong><span>AI compatibility</span></div>
      </section>

      <div className="profile-grid">
        <section className="panel">
          <h2>Skills</h2>
          {skills.map(([skill, score]) => (
            <div className="skill-meter" key={skill}>
              <div><span>{skill}</span><strong>{score}%</strong></div>
              <div className="match-bar"><span style={{ width: `${score}%` }} /></div>
            </div>
          ))}
        </section>

        <section className="panel">
          <h2>Evidence</h2>
          <div className="evidence-item"><span>▤</span><div><strong>Academic Transcript</strong><small>Verified academic evidence</small></div></div>
          <div className="evidence-item"><span>▤</span><div><strong>CV / Resume</strong><small>Candidate-provided document</small></div></div>
          <div className="evidence-item"><span>★</span><div><strong>Power BI Project</strong><small>Portfolio evidence</small></div></div>
        </section>
      </div>

      <section className="panel explanation-panel">
        <span className="eyebrow">EXPLAINABLE MATCH</span>
        <h2>Why this candidate matches</h2>
        <p>Strong alignment with SQL, Excel and statistics requirements. The main development area is Power BI, which is currently below the requested level.</p>
        <div className="recommendation-box"><strong>Recommended next step</strong><span>Review the candidate's Power BI project before making a final decision.</span></div>
      </section>
    </div>
  );
}