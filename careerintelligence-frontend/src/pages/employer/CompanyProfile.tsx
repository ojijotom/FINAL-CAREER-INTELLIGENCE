import { useState } from "react";

export default function CompanyProfile() {
  const [saved, setSaved] = useState(false);

  return (
    <div className="page narrow-page">
      <div className="page-heading">
        <div><span className="eyebrow">COMPANY PROFILE</span><h1>Tell candidates about your company.</h1><p>A complete profile helps candidates understand who is hiring.</p></div>
      </div>
      <section className="panel form-panel">
        <div className="company-profile-header">
          <div className="large-company-avatar">TS</div>
          <div><h2>Tech Solutions Ltd.</h2><p>Technology · Nairobi, Kenya</p></div>
        </div>
        <div className="form-grid">
          <label>Company name<input defaultValue="Tech Solutions Ltd." /></label>
          <label>Industry<input defaultValue="Information Technology" /></label>
          <label>Location<input defaultValue="Nairobi, Kenya" /></label>
          <label>Website<input defaultValue="https://example.com" /></label>
        </div>
        <label>Company description<textarea defaultValue="We build technology solutions that help organizations solve real-world problems." /></label>
        <div className="form-actions"><button className="primary-button" onClick={() => setSaved(true)}>{saved ? "Saved" : "Save changes"}</button></div>
      </section>
    </div>
  );
}