import { useState } from "react";
import type { FormEvent } from "react";
import { Link } from "react-router-dom";

export default function PostJob() {
  const [submitted, setSubmitted] = useState(false);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitted(true);
  }

  return (
    <div className="page narrow-page">
      <div className="page-heading">
        <div><span className="eyebrow">NEW OPPORTUNITY</span><h1>Post a job.</h1><p>Define the role and skills you need. The system will use them for talent matching.</p></div>
      </div>

      {submitted && <div className="success-message"><strong>Job saved as a draft.</strong><span>Later, the backend will validate and publish this opportunity.</span></div>}

      <form className="panel form-panel" onSubmit={handleSubmit}>
        <div className="form-grid">
          <label>Job title<input required placeholder="e.g. Data Analyst" /></label>
          <label>Department<input placeholder="e.g. Data & Analytics" /></label>
          <label>Employment type<select defaultValue="Full-time"><option>Full-time</option><option>Part-time</option><option>Contract</option><option>Internship</option></select></label>
          <label>Location<input placeholder="e.g. Nairobi, Kenya" /></label>
        </div>
        <label>Job description<textarea required placeholder="Describe the role, responsibilities and expectations." /></label>
        <label>Required skills<input required placeholder="SQL, Excel, Power BI, Statistics" /></label>
        <label>Education / qualifications<input placeholder="Relevant degree, diploma or equivalent experience" /></label>
        <div className="ai-info"><strong>Skills intelligence</strong><p>When the backend is connected, Career Intelligence will normalize the skills in this job and use them to rank candidates.</p></div>
        <div className="form-actions"><Link className="secondary-button" to="/employer/jobs">Cancel</Link><button className="primary-button" type="submit">Save Job</button></div>
      </form>
    </div>
  );
}