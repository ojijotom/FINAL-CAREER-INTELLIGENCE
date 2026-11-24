import type { Skill } from "../types";
import ProgressBar from "./ProgressBar";

export default function SkillCard({ skill }: { skill: Skill }) {
  const gap = Math.max(0, skill.target - skill.level);

  return (
    <article className="card">
      <div className="skill-title">
        <div>
          <h3>{skill.name}</h3>
          <span className="muted">{skill.evidence}</span>
        </div>
        <strong>{skill.level}%</strong>
      </div>
      <ProgressBar value={skill.level} />
      <div className="skill-meta">
        <span>Target: {skill.target}%</span>
        <span>{gap > 0 ? `${gap}% gap` : "Target reached"}</span>
      </div>
    </article>
  );
}