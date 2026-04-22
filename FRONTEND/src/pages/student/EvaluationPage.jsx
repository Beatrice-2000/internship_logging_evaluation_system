export default function EvaluationPage() {
  // Week 9 — Score Computation
  const criteria = [
    { label: 'Workplace Supervisor Score', weight: '40%', score: null },
    { label: 'Academic Supervisor Score',  weight: '30%', score: null },
    { label: 'Logbook Score',              weight: '30%', score: null },
  ];

  return (
    <div>
      <h1 className="page-title">My Evaluation</h1>
      <div className="card">
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              {['Criteria', 'Weight', 'Score', 'Weighted Score'].map(h => (
                <th key={h} style={{ padding: '10px 14px', textAlign: 'left', fontSize: 12, fontWeight: 700, color: '#64748b', textTransform: 'uppercase', borderBottom: '1px solid #e2e8f0' }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {criteria.map(c => (
              <tr key={c.label}>
                <td style={{ padding: '12px 14px', borderBottom: '1px solid #f1f5f9' }}>{c.label}</td>
                <td style={{ padding: '12px 14px', borderBottom: '1px solid #f1f5f9' }}>{c.weight}</td>
                <td style={{ padding: '12px 14px', borderBottom: '1px solid #f1f5f9', color: '#94a3b8' }}>Pending</td>
                <td style={{ padding: '12px 14px', borderBottom: '1px solid #f1f5f9', color: '#94a3b8' }}>—</td>
              </tr>
            ))}
            <tr>
              <td colSpan={3} style={{ padding: '12px 14px', fontWeight: 700 }}>Total Score</td>
              <td style={{ padding: '12px 14px', fontWeight: 700, fontSize: 18 }}>—</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
