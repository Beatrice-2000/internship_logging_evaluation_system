export default function SupervisorDashboard() {
  const stats = [
    { label: 'Assigned Interns',  value: 0, icon: '🎓', color: '#dbeafe' },
    { label: 'Pending Reviews',   value: 0, icon: '⏳', color: '#fef9c3' },
    { label: 'Reviewed This Week',value: 0, icon: '✅', color: '#dcfce7' },
  ];
  return (
    <div>
      <h1 className="page-title">Supervisor Dashboard</h1>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 24 }}>
        {stats.map(s => (
          <div key={s.label} className="card" style={{ background: s.color, border: 'none' }}>
            <div style={{ fontSize: 28, marginBottom: 8 }}>{s.icon}</div>
            <div style={{ fontSize: 28, fontWeight: 700 }}>{s.value}</div>
            <div style={{ fontSize: 13, marginTop: 4 }}>{s.label}</div>
          </div>
        ))}
      </div>
      <div className="card">
        <h3 style={{ fontWeight: 700, marginBottom: 12 }}>Your Interns</h3>
        <p style={{ color: '#64748b' }}>No interns assigned yet.</p>
      </div>
    </div>
  );
}
