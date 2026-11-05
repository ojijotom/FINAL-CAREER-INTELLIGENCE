import { Link } from "react-router-dom";
import { skills } from "../../data/mockData";
import ProgressBar from "../../components/ProgressBar";

export default function SkillGap() {
  const gaps = [...skills].sort((a, b) => (b.target - b.level) - (a.target - a.level));

  return (
    <div className="page">
      <div className="page-header"><div><span className="eyebrow">GAP ANALYSIS</span><h1>Your skill gaps</h1><p>Prioritized development areas for your current target career.</p></div></div>
      <div className="card explanation">
        <div className="action-icon">✦</div>
        <div><h3>How the analysis works</h3><p>The prototype compares your current skill evidence with target levels. A production version will combine validated labour-market data, occupation taxonomies and assessment evidence.</p></div>
      </div>
      <div className="gap-list">
        {gaps.map((skill, index) => {
          const gap = Math.max(0, skill.target - skill.level);
          return <article className="card gap-item" key={skill.name}>
            <div className="gap-number">{index + 1}</div>
            <div className="gap-content"><div className="skill-title"><div><h3>{skill.name}</h3><span className="muted">{skill.evidence}</span></div><strong>{gap}% gap</strong></div><ProgressBar value={skill.level} label={`Current ${skill.level}% · Target ${skill.target}%`} /><p>{gap > 0 ? `Focus on practical activities that can produce evidence for ${skill.name}.` : "Your current level meets the target."}</p></div>
            <Link to="/student/jobs" className="text-link">Find opportunities →</Link>
          </article>;
        })}
      </div>
    </div>
  );
}