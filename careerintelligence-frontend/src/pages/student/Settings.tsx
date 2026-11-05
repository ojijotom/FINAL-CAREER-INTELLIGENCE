export default function Settings() {
  return (
    <div className="page narrow-page">
      <div className="page-header"><div><span className="eyebrow">ACCOUNT</span><h1>Settings</h1><p>Manage preferences and responsible use of your career data.</p></div></div>
      <div className="card settings-list">
        <div><div><h3>Recommendation explanations</h3><p>Show the evidence and factors behind career recommendations.</p></div><input type="checkbox" defaultChecked /></div>
        <div><div><h3>Profile visibility</h3><p>Control whether your profile can be used for future matching features.</p></div><input type="checkbox" /></div>
        <div><div><h3>Notifications</h3><p>Receive updates about new opportunities and development tasks.</p></div><input type="checkbox" defaultChecked /></div>
        <div><div><h3>Data correction</h3><p>You should be able to review and correct information used by the system.</p></div><button className="secondary-button">Review data</button></div>
      </div>
    </div>
  );
}