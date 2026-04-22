import { useState } from 'react';

const PENDING_LOGS = [
  { id: 3, student: 'Alice Nakato',  week: 3, title: 'Backend Work',  submitted: '2026-01-24' },
  { id: 5, student: 'Bob Ssempijja', week: 3, title: 'API Integration', submitted: '2026-01-25' },
];

export default function SupervisorReviews() {
  const [logs, setLogs]         = useState(PENDING_LOGS);
  const [selected, setSelected] = useState(null);
  const [comment, setComment]   = useState('');

  const handleReview = (action) => {
    alert(`Log ${action}! (Connect to Django API)`);
    setLogs((l) => l.filter((x) => x.id !== selected.id));
    setSelected(null);
    setComment('');
  };

  return (
    <div>
      <h1 className="page-title">Log Reviews</h1>

      <div style={{ display: 'grid', gridTemplateColumns: selected ? '1fr 1fr' : '1fr', gap: 24 }}>
        {/* List */}
        <div className="card">
          <h3 style={{ fontWeight: 700, marginBottom: 16 }}>
            Pending Reviews ({logs.length})
          </h3>
          {logs.length === 0 && (
            <p style={{ color: '#64748b' }}>All logs reviewed. Great work! ✅</p>
          )}
          {logs.map((log) => (
            <div
              key={log.id}
              onClick={() => setSelected(log)}
              style={{
                padding: '14px',
                borderRadius: 8,
                border: `1.5px solid ${selected?.id === log.id ? '#1a56db' : '#e2e8f0'}`,
                marginBottom: 10,
                cursor: 'pointer',
                background: selected?.id === log.id ? '#e8effd' : '#fff',
                transition: 'all 0.15s',
              }}
            >
              <div style={{ fontWeight: 600 }}>{log.student}</div>
              <div style={{ fontSize: 13, color: '#64748b' }}>Week {log.week} — {log.title}</div>
              <div style={{ fontSize: 12, color: '#94a3b8', marginTop: 4 }}>Submitted: {log.submitted}</div>
            </div>
          ))}
        </div>

        {/* Review panel */}
        {selected && (
          <div className="card">
            <h3 style={{ fontWeight: 700, marginBottom: 4 }}>{selected.student}</h3>
            <p style={{ color: '#64748b', marginBottom: 20 }}>Week {selected.week} — {selected.title}</p>

            <div style={{ background: '#f8fafc', borderRadius: 8, padding: 16, marginBottom: 20 }}>
              <p style={{ color: '#64748b', fontStyle: 'italic' }}>
                [Log content loads here from Django API]
              </p>
            </div>

            <div className="form-group">
              <label>Review Comment</label>
              <textarea
                className="form-control"
                rows={4}
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="Write your review comment..."
              />
            </div>

            <div style={{ display: 'flex', gap: 10 }}>
              <button className="btn btn-success" onClick={() => handleReview('approved')}>
                ✅ Approve
              </button>
              <button className="btn btn-danger" onClick={() => handleReview('rejected')}>
                ❌ Reject
              </button>
              <button className="btn btn-outline" onClick={() => setSelected(null)}>
                Cancel
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
