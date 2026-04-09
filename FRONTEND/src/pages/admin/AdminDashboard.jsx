export default function AdminDashboard() {
  const stats = [
    { label: 'Total Students',    value: 0, icon: '🎓', color: '#dbeafe' },
    { label: 'Active Placements', value: 0, icon: '🏢', color: '#dcfce7' },
    { label: 'Logs This Week',    value: 0, icon: '📓', color: '#fef9c3' },
    { label: 'Pending Reviews',   value: 0, icon: '⏳', color: '#fee2e2' },
  ];

  return (
    <div>
      <h1 className="page-title">Administrator Dashboard</h1>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))', gap: 16, marginBottom: 28 }}>
        {stats.map((s) => (
          <div key={s.label} className="card" style={{ background: s.color, border: 'none' }}>
            <div style={{ fontSize: 28, marginBottom: 8 }}>{s.icon}</div>
            <div style={{ fontSize: 28, fontWeight: 700 }}>{s.value}</div>
            <div style={{ fontSize: 13, color: '#374151', marginTop: 4 }}>{s.label}</div>
          </div>
        ))}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24 }}>
        <div className="card">
          <h3 style={{ fontWeight: 700, marginBottom: 12 }}>Recent Activity</h3>
          <p style={{ color: '#64748b' }}>No recent activity yet.</p>
        </div>
        <div className="card">
          <h3 style={{ fontWeight: 700, marginBottom: 12 }}>Quick Actions</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
            <button className="btn btn-primary">+ Assign Placement</button>
            <button className="btn btn-outline">👥 Manage Users</button>
            <button className="btn btn-outline">📈 View Reports</button>
          </div>
        </div>
      </div>
    </div>
  );
}
