export default function AcademicDashboard() {
  return (
    <div>
      <h1 className="page-title">Academic Supervisor Dashboard</h1>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24 }}>
        <div className="card">
          <h3 style={{ fontWeight: 700, marginBottom: 12 }}>Pending Evaluations</h3>
          <p style={{ color: '#64748b' }}>No evaluations pending.</p>
        </div>
        <div className="card">
          <h3 style={{ fontWeight: 700, marginBottom: 12 }}>Completed Evaluations</h3>
          <p style={{ color: '#64748b' }}>No completed evaluations yet.</p>
        </div>
      </div>
    </div>
  );
}
