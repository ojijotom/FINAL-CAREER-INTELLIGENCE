import ProgressBar from "./ProgressBar";

interface SkillCardData {
  name: string;
  level: number | null;
  target?: number | null;
  evidence: string;
}

export default function SkillCard({
  skill,
}: {
  skill: SkillCardData;
}) {
  const hasLevel = skill.level !== null;
  const hasTarget = skill.target !== null && skill.target !== undefined;

  const gap =
    hasLevel && hasTarget
      ? Math.max(0, skill.target! - skill.level!)
      : null;

  return (
    <article className="card">
      <div className="skill-title">
        <div>
          <h3>{skill.name}</h3>
          <span className="muted">{skill.evidence}</span>
        </div>

        <strong>
          {hasLevel ? `${skill.level}%` : "Not assessed"}
        </strong>
      </div>

      <ProgressBar value={skill.level ?? 0} />

      <div className="skill-meta">
        <span>
          {hasTarget ? `Target: ${skill.target}%` : "Target not set"}
        </span>

        <span>
          {gap === null
            ? "Awaiting assessment"
            : gap > 0
              ? `${gap}% gap`
              : "Target reached"}
        </span>
      </div>
    </article>
  );
}