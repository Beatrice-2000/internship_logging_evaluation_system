import { useState } from 'react';

const MOCK_LOGS = [
  { id: 1, week: 1, title: 'Orientation Week', status: 'approved',  submitted: '2026-01-10' },
  { id: 2, week: 2, title: 'Project Setup',    status: 'reviewed',  submitted: '2026-01-17' },
  { id: 3, week: 3, title: 'Backend Work',     status: 'submitted', submitted: '2026-01-24' },
  { id: 4, week: 4, title: 'Frontend Work',    status: 'draft',     submitted: null },
];

export default function LogbookPage() {
  const [logs]         = useState(MOCK_LOGS);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ title: '', activities: '', challenges: '', week: '' });

  const handleChange = (e) =>
    setForm((f) => ({ ...f, [e.target.name]: e.target.value }));

  const handleSubmit = (e) => {
    e.preventDefault();
    alert('Log saved! (Connect to Django API to persist)');
    setShowForm(false);
  };

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <h1 className="page-title" style={{ margin: 0 }}>Weekly Logbook</h1>
        <button className="btn btn-primary" onClick={() => setShowForm((s) => !s)}>
          + New Log Entry
        </button>
      </div>

      {/* New log form */}
      {showForm && (
        <div className="card" style={{ marginBottom: 24, borderLeft: '4px solid #1a56db' }}>
          <h3 style={{ marginBottom: 16, fontWeight: 700 }}>New Weekly Log</h3>
          <form onSubmit={handleSubmit}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
              <div className="form-group">
                <label>Week Number</label>
                <input
                  className="form-control"
                  name="week" type="number" min="1" max="20"
                  value={form.week} onChange={handleChange}
                  placeholder="e.g. 5" required
                />
              </div>
              <div className="form-group">
                <label>Log Title</label>
                <input
                  className="form-control"
                  name="title" value={form.title}
                  onChange={handleChange}
                  placeholder="Brief title for this week" required
                />
              </div>
            </div>
            <div className="form-group">
              <label>Activities Performed</label>
              <textarea
                className="form-control"
                name="activities" value={form.activities}
                onChange={handleChange}
                rows={4}
                placeholder="Describe what you did this week..."
                required
              />
            </div>
            <div className="form-group">
              <label>Challenges Encountered</label>
              <textarea
                className="form-control"
                name="challenges" value={form.challenges}
                onChange={handleChange}
                rows={3}
                placeholder="Describe any challenges or learnings..."
              />
            </div>
            <div style={{ display: 'flex', gap: 10 }}>
              <button type="submit" className="btn btn-primary">Save as Draft</button>
              <button type="button" className="btn btn-outline" onClick={() => setShowForm(false)}>Cancel</button>
            </div>
          </form>
        </div>
      )}

      {/* Logs table */}
      <div className="card">
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              {['Week', 'Title', 'Status', 'Submitted', 'Actions'].map((h) => (
                <th key={h} style={{ padding: '10px 14px', textAlign: 'left', fontSize: 12, fontWeight: 700, color: '#64748b', textTransform: 'uppercase', borderBottom: '1px solid #e2e8f0' }}>
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {logs.map((log) => (
              <tr key={log.id} style={{ transition: 'background 0.15s' }}>
                <td style={{ padding: '12px 14px', borderBottom: '1px solid #f1f5f9' }}>Week {log.week}</td>
                <td style={{ padding: '12px 14px', borderBottom: '1px solid #f1f5f9', fontWeight: 500 }}>{log.title}</td>
                <td style={{ padding: '12px 14px', borderBottom: '1px solid #f1f5f9' }}>
                  <span className={`badge badge-${log.status}`}>{log.status}</span>
                </td>
                <td style={{ padding: '12px 14px', borderBottom: '1px solid #f1f5f9', color: '#64748b' }}>
                  {log.submitted || '—'}
                </td>
                <td style={{ padding: '12px 14px', borderBottom: '1px solid #f1f5f9' }}>
                  {log.status === 'draft' && (
                    <button className="btn btn-outline" style={{ padding: '5px 12px', fontSize: 13 }}>Edit</button>
                  )}
                  {log.status !== 'draft' && (
                    <button className="btn btn-outline" style={{ padding: '5px 12px', fontSize: 13 }}>View</button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
