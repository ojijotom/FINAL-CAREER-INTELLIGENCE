import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";

export default function LandingPage() {
  return (
    <div className="landing-page">
      <Navbar />
      <main>
        <section className="hero">
          <div className="hero-copy">
            <span className="eyebrow">AI-BASED CAREER & SKILLS GAP ADVISER</span>
            <h1>Turn your academic journey into a <span>career pathway.</span></h1>
            <p>
              Understand your skills, discover suitable career paths, identify
              your gaps and get evidence-based development recommendations.
            </p>
            <div className="hero-actions">
              <Link to="/register" className="primary-button">Get started</Link>
              <Link to="/login" className="secondary-button">Sign in</Link>
            </div>
            <div className="hero-trust">
              <span>✓ Skills analysis</span>
              <span>✓ Career matching</span>
              <span>✓ Explainable recommendations</span>
            </div>
          </div>

          <div className="hero-panel">
            <div className="panel-header">
              <div>
                <span className="muted">Career Intelligence</span>
                <h3>Data Analyst</h3>
              </div>
              <span className="score-circle">78%</span>
            </div>
            <div className="insight-box">
              <span className="insight-icon">✦</span>
              <div>
                <strong>Next best action</strong>
                <p>Build your Power BI skills through a practical project.</p>
              </div>
            </div>
            <div className="mock-bars">
              <div><span>SQL</span><i style={{ width: "72%" }} /></div>
              <div><span>Excel</span><i style={{ width: "88%" }} /></div>
              <div><span>Power BI</span><i style={{ width: "43%" }} /></div>
              <div><span>Statistics</span><i style={{ width: "76%" }} /></div>
            </div>
          </div>
        </section>

        <section className="feature-section">
          <div className="section-heading">
            <span className="eyebrow">HOW IT WORKS</span>
            <h2>From student evidence to career direction</h2>
          </div>
          <div className="feature-grid">
            <div className="feature card"><span>01</span><h3>Build your profile</h3><p>Bring together your programme, courses, skills, projects and evidence.</p></div>
            <div className="feature card"><span>02</span><h3>Understand the market</h3><p>Compare your profile with skills and requirements associated with career opportunities.</p></div>
            <div className="feature card"><span>03</span><h3>Close the gaps</h3><p>Receive prioritized learning and practical development pathways.</p></div>
          </div>
        </section>
      </main>
    </div>
  );
}