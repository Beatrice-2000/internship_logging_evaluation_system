import { useAuth } from '../../context/AuthContext';

export default function StudentDashboard() {
  const { user } = useAuth();

  const stats = [
    { label: 'Logs Submitted',  value: 0, icon: '📓', color: '#dbeafe' },
    { label: 'Logs Approved',   value: 0, icon: '✅', color: '#dcfce7' },
    { label: 'Pending Reviews', value: 0, icon: '⏳', color: '#fef9c3' },
    { label: 'Overall Score',   value: '—', icon: '🏆', color: '#f3e8ff' },
  ];

  return (
    <div>
      <h1 className="page-title">
        Welcome back, {user?.first_name || user?.username} 👋
      </h1>

      {/* Stats row */}
      <div style={styles.statsGrid}>
        {stats.map((s) => (
          <div key={s.label} className="card" style={{ background: s.color, border: 'none' }}>
            <div style={styles.statIcon}>{s.icon}</div>
            <div style={styles.statValue}>{s.value}</div>
            <div style={styles.statLabel}>{s.label}</div>
          </div>
        ))}
      </div>

      {/* Placement info */}
      <div className="card" style={{ marginTop: 24 }}>
        <h3 style={styles.sectionTitle}>My Internship Placement</h3>
        <p style={{ color: '#64748b' }}>No active placement found. Please contact your administrator.</p>
      </div>

      {/* Recent logs */}
      <div className="card" style={{ marginTop: 24 }}>
        <h3 style={styles.sectionTitle}>Recent Weekly Logs</h3>
        <table style={styles.table}>
          <thead>
            <tr>
              {['Week', 'Title', 'Status', 'Submitted'].map((h) => (
                <th key={h} style={styles.th}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            <tr>
              <td colSpan={4} style={{ ...styles.td, color: '#64748b', textAlign: 'center' }}>
                No logs yet. Start by submitting your Week 1 log.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}

const styles = {
  statsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))',
    gap: 16,
  },
  statIcon:  { fontSize: 28, marginBottom: 8 },
  statValue: { fontSize: 28, fontWeight: 700, lineHeight: 1 },
  statLabel: { fontSize: 13, color: '#374151', marginTop: 4 },
  sectionTitle: { fontSize: 16, fontWeight: 700, marginBottom: 16 },
  table: { width: '100%', borderCollapse: 'collapse' },
  th: {
    padding: '10px 14px', textAlign: 'left',
    fontSize: 12, fontWeight: 700,
    color: '#64748b', textTransform: 'uppercase',
    borderBottom: '1px solid #e2e8f0',
  },
  td: {
    padding: '12px 14px',
    borderBottom: '1px solid #f1f5f9',
    fontSize: 14,
  },
};
