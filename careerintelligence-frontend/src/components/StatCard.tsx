interface StatCardProps {
  label: string;
  value: string;
  note: string;
  icon: string;
}

export default function StatCard({ label, value, note, icon }: StatCardProps) {
  return (
    <div className="stat-card">
      <div className="stat-card-top">
        <span className="stat-icon">{icon}</span>
        <span className="stat-note">{note}</span>
      </div>
      <div className="stat-value">{value}</div>
      <div className="stat-label">{label}</div>
    </div>
  );
}