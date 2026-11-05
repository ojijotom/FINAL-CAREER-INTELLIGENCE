import { Link } from "react-router-dom";

export default function TalentSearch() {
  return (
    <div className="page">
      <div className="page-heading">
        <div><span className="eyebrow">TALENT INTELLIGENCE</span><h1>Find talent by skills.</h1><p>Search beyond job titles and discover candidates with relevant evidence.</p></div>
      </div>
      <section className="panel search-panel">
        <label>What skills do you need?<input placeholder="Try: Python, SQL, React, cybersecurity..." /></label>
        <div className="skill-chips"><span>Python</span><span>SQL</span><span>Data Analysis</span><span>React</span><span>Cybersecurity</span></div>
        <button className="primary-button">Search talent</button>
      </section>
      <section className="panel">
        <div className="panel-heading"><div><h2>How Talent Search will work</h2><p>This is the frontend prototype. Matching will be connected to the backend later.</p></div></div>
        <div className="search-flow">
          <div><b>1</b><span>Employer defines required skills</span></div>
          <div><b>2</b><span>System normalizes the skills</span></div>
          <div><b>3</b><span>Candidate profiles are compared</span></div>
          <div><b>4</b><span>Evidence and compatibility are ranked</span></div>
        </div>
      </section>
      <Link className="secondary-button" to="/employer/candidates">Browse current candidates</Link>
    </div>
  );
}