import { useState } from "react";

export default function EmployerSettings() {
  const [notifications, setNotifications] = useState(true);

  return (
    <div className="page narrow-page">
      <div className="page-heading">
        <div><span className="eyebrow">ACCOUNT</span><h1>Settings</h1><p>Manage employer account preferences.</p></div>
      </div>
      <section className="panel settings-list">
        <div className="setting-row">
          <div><strong>Application notifications</strong><span>Receive updates when candidates apply.</span></div>
          <button className={notifications ? "toggle on" : "toggle"} onClick={() => setNotifications(!notifications)}><span /></button>
        </div>
        <div className="setting-row">
          <div><strong>Candidate visibility</strong><span>Control which candidate evidence recruiters can access.</span></div>
          <span className="setting-value">Managed by admin</span>
        </div>
        <div className="setting-row">
          <div><strong>Responsible AI</strong><span>Recommendations are decision-support and should not replace human review.</span></div>
          <span className="setting-value">Enabled</span>
        </div>
      </section>
    </div>
  );
}