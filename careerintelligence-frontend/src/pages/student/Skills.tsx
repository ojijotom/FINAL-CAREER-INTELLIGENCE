import { useEffect, useState } from "react";

import SkillCard from "../../components/SkillCard";

import {
  getSkillCatalogue,
  getStudentSkills,
  type SkillCatalogueItem,
  type StudentSkillRecord,
} from "../../api";

import { useAuth } from "../../auth/AuthContext";

interface DisplaySkill {
  id: number;
  name: string;
  level: number | null;
  target: null;
  evidence: string;
  verified: boolean;
}

export default function Skills() {
  const { accessToken } = useAuth();

  const [skills, setSkills] = useState<DisplaySkill[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function loadSkills() {
      if (!accessToken) {
        setError("Please log in to view your skills.");
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setError("");

        const [studentSkills, catalogue] = await Promise.all([
          getStudentSkills(accessToken),
          getSkillCatalogue(accessToken),
        ]);

        if (cancelled) return;

        const catalogueMap = new Map<number, SkillCatalogueItem>(
          catalogue.map((skill) => [skill.id, skill]),
        );

        const realSkills: DisplaySkill[] = studentSkills.map((record) => {
          const catalogueSkill = catalogueMap.get(record.skill);

          return {
            id: record.id,
            name: catalogueSkill?.name ?? `Skill #${record.skill}`,
            level: record.level,
            target: null,
            evidence:
              record.evidence_description?.trim() ||
              (record.verified
                ? "Verified evidence"
                : `Source: ${record.source.replaceAll("_", " ")}`),
            verified: record.verified,
          };
        });

        setSkills(realSkills);
      } catch (err) {
        if (!cancelled) {
          setError(
            err instanceof Error
              ? err.message
              : "Unable to load your skills.",
          );
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadSkills();

    return () => {
      cancelled = true;
    };
  }, [accessToken]);

  const assessedSkills = skills.filter(
    (skill) => skill.level !== null,
  );

  const average =
    assessedSkills.length > 0
      ? Math.round(
          assessedSkills.reduce(
            (sum, skill) => sum + (skill.level ?? 0),
            0,
          ) / assessedSkills.length,
        )
      : null;

  const verifiedCount = skills.filter(
    (skill) => skill.verified,
  ).length;

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <span className="eyebrow">SKILL PASSPORT</span>
          <h1>Your skills</h1>
          <p>
            Track skills, proficiency and the evidence supporting each skill.
          </p>
        </div>
      </div>

      {loading && (
        <div className="card">
          <p>Loading your skills from the database...</p>
        </div>
      )}

      {!loading && error && (
        <div className="card">
          <h3>Unable to load skills</h3>
          <p>{error}</p>
          <button
            className="secondary-button"
            onClick={() => window.location.reload()}
          >
            Try again
          </button>
        </div>
      )}

      {!loading && !error && (
        <>
          <div className="dashboard-grid">
            <div className="stat-card highlight">
              <span>Average skill level</span>
              <strong>
                {average !== null ? `${average}%` : "—"}
              </strong>
              <small>
                {assessedSkills.length} assessed skills
              </small>
            </div>

            <div className="stat-card">
              <span>Verified skills</span>
              <strong>{verifiedCount}</strong>
              <small>Skills verified by the system</small>
            </div>

            <div className="stat-card">
              <span>Skills tracked</span>
              <strong>{skills.length}</strong>
              <small>Your recorded skills</small>
            </div>
          </div>

          {skills.length === 0 ? (
            <div className="card">
              <h3>No skills recorded yet</h3>
              <p>
                Your skill passport is currently empty.
                Skills will appear here when you add them to your profile.
              </p>
            </div>
          ) : (
            <div className="cards-grid two">
              {skills.map((skill) => (
                <SkillCard
                  key={skill.id}
                  skill={{
                    name: skill.name,
                    level: skill.level,
                    target: skill.target,
                    evidence: skill.evidence,
                  }}
                />
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}