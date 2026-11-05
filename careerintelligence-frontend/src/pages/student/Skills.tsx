import SkillCard from "../../components/SkillCard";
import { skills } from "../../data/mockData";

export default function Skills() {
  const average = Math.round(skills.reduce((sum, skill) => sum + skill.level, 0) / skills.length);

  return (
    <div className="page">
      <div className="page-header"><div><span className="eyebrow">SKILL PASSPORT</span><h1>Your skills</h1><p>Track skills, proficiency and the evidence supporting each skill.</p></div></div>
      <div className="dashboard-grid">
        <div className="stat-card highlight"><span>Average skill level</span><strong>{average}%</strong><small>Across your current skill profile</small></div>
        <div className="stat-card"><span>Verified evidence</span><strong>7</strong><small>Academic and practical</small></div>
        <div className="stat-card"><span>Skills tracked</span><strong>{skills.length}</strong><small>Target career skills</small></div>
      </div>
      <div className="cards-grid two">{skills.map(skill => <SkillCard key={skill.name} skill={skill} />)}</div>
    </div>
  );
}