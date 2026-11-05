import { Link, useParams } from "react-router-dom";
import { careers, skills } from "../../data/mockData";
import ProgressBar from "../../components/ProgressBar";

export default function CareerDetail() {
  const { careerId } = useParams();
  const career = careers.find(item => item.id === careerId) ?? careers[0];

  return (
    <div className="page">
      <Link to="/student/careers" className="back-link">← Back to careers</Link>
      <div className="detail-hero card">
        <div><span className="badge">{career.demand} demand</span><h1>{career.title}</h1><p>{career.description}</p></div>
        <div className="large-score"><strong>{career.compatibility}%</strong><span>compatibility</span></div>
      </div>
      <div className="detail-grid">
        <section>
          <div className="section-heading compact"><div><span className="eyebrow">SKILL REQUIREMENTS</span><h2>What this career needs</h2></div></div>
          <div className="skill-list">{career.skills.map(name => {
            const skill = skills.find(s => s.name === name);
            return <div className="card skill-row" key={name}><div><strong>{name}</strong><span className="muted">{skill?.evidence ?? "Market requirement"}</span></div><ProgressBar value={skill?.level ?? 40} /><span>{skill?.level ?? 40}%</span></div>;
          })}</div>
        </section>
        <aside className="card">
          <span className="eyebrow">YOUR PATHWAY</span>
          <h3>Recommended next step</h3>
          <p>Prioritize the skills with the largest evidence-backed gap, then build practical evidence through projects and assessments.</p>
          <Link to="/student/skill-gap" className="primary-button full">Analyze my gaps</Link>
        </aside>
      </div>
    </div>
  );
}