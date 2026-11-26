
import { useEffect, useState } from "react";
import { getStudentSkills, type StudentSkill } from "../../api";
import { useAuth } from "../../auth/AuthContext";

export default function Skills() {
  const { accessToken } = useAuth();

  const [skills, setSkills] = useState<StudentSkill[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!accessToken) {
      setLoading(false);
      return;
    }

    getStudentSkills(accessToken)
      .then((data) => {
        setSkills(data);
      })
      .catch(() => {
        setError("Failed to load your skills. Please try again.");
      })
      .finally(() => {
        setLoading(false);
      });
  }, [accessToken]);

  const assessedSkills = skills.filter(
    (skill) => skill.level !== null
  );

  const average =
    assessedSkills.length > 0
      ? Math.round(
          assessedSkills.reduce(
            (sum, skill) => sum + (skill.level ?? 0),
            0
          ) / assessedSkills.length
        )
      : null;

  const verifiedCount = skills.filter(
    (skill) => skill.verified
  ).length;

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <span className="eyebrow">SKILL PASSPORT</span>
          <h1>Your skills</h1>
          <p>
            Track your skills, proficiency and evidence supporting
            each skill.
          </p>
        </div>
      </div>

      <div className="dashboard-grid">
        <div className="stat-card highlight">
          <span>Average skill level</span>
          <strong>{average !== null ? `${average}%` : "N/A"}</strong>
          <small>
            Based on assessed skills
          </small>
        </div>

        <div className="stat-card">
          <span>Verified skills</span>
          <strong>{verifiedCount}</strong>
          <small>Skills verified by evidence</small>
        </div>

        <div className="stat-card">
          <span>Skills tracked</span>
          <strong>{skills.length}</strong>
          <small>Your current skill profile</small>
        </div>
      </div>

      {loading && (
        <div className="stat-card">
          <p>Loading your skills...</p>
        </div>
      )}

      {error && (
        <div className="stat-card">
          <p>{error}</p>
        </div>
      )}

      {!loading && !error && skills.length === 0 && (
        <div className="stat-card">
          <h3>No skills found yet</h3>
          <p>
            Upload your CV or transcript to start building your
            skill profile.
          </p>
        </div>
      )}

      {!loading && !error && skills.length > 0 && (
        <div className="cards-grid two skills-grid">
          {skills.map((skill) => (
             <div className="stat-card skill-detail-card" key={skill.id}>
              <div className="page-header">
                <div>
                  <h3>{skill.skill_name}</h3>
                  <small>{skill.skill_category}</small>
                </div>
              </div>

              <p>
                <strong>Proficiency:</strong>{" "}
                {skill.level !== null
                  ? `${skill.level}%`
                  : "Not assessed"}
              </p>

              <p>
                <strong>Source:</strong>{" "}
                {skill.source.replace(/_/g, " ")}
              </p>

              <p>
                <strong>Verification:</strong>{" "}
                {skill.verified ? "Verified" : "Not verified"}
              </p>

              {skill.evidence_description && (
                <p>
                  <strong>Evidence:</strong>{" "}
                  {skill.evidence_description}
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
