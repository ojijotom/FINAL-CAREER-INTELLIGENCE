import { Link } from "react-router-dom";
import type { Career } from "../types";

export default function CareerCard({ career }: { career: Career }) {
  return (
    <article className="card career-card">
      <div className="card-top">
        <div className="icon-box">◎</div>
        <span className="badge">{career.demand} demand</span>
      </div>
      <h3>{career.title}</h3>
      <p>{career.description}</p>
      <div className="compatibility">
        <span>Compatibility</span>
        <strong>{career.compatibility}%</strong>
      </div>
      <div className="skill-chips">
        {career.skills.slice(0, 4).map((skill) => <span key={skill}>{skill}</span>)}
      </div>
      <Link to={`/careers/${career.id}`} className="text-link">Explore career →</Link>
    </article>
  );
}