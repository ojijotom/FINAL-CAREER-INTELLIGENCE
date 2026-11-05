import { useState } from "react";
import type { FormEvent } from "react";
import { studentProfile } from "../../data/mockData";

export default function Profile() {
  const [saved, setSaved] = useState(false);

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSaved(true);
    window.setTimeout(() => setSaved(false), 2500);
  };

  return (
    <div className="page narrow-page">
      <div className="page-header"><div><span className="eyebrow">STUDENT PROFILE</span><h1>Your profile</h1><p>Keep the information used by the career intelligence engine up to date.</p></div></div>
      {saved && <div className="success-message">Profile saved successfully in this prototype.</div>}
      <form className="card form profile-form" onSubmit={handleSubmit}>
        <div className="profile-avatar">AS</div>
        <div className="two-inputs"><label>First name<input defaultValue="Alex" /></label><label>Last name<input defaultValue="Student" /></label></div>
        <label>Email<input type="email" defaultValue="alex@example.com" /></label>
        <label>University<input defaultValue={studentProfile.university} /></label>
        <label>Programme<input defaultValue={studentProfile.programme} /></label>
        <label>Target career<select defaultValue="Data Analyst"><option>Data Analyst</option><option>Software Developer</option><option>Cybersecurity Analyst</option></select></label>
        <button className="primary-button" type="submit">Save profile</button>
      </form>
    </div>
  );
}