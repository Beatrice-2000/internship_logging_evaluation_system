import { useEffect, useState } from 'react';
import API from '../../Services/Api';

const STATUS_COLORS = {
  pending:   { background: '#fef9c3', color: '#ca8a04' },
  active:    { background: '#dcfce7', color: '#16a34a' },
  completed: { background: '#dbeafe', color: '#2563eb' },
  cancelled: { background: '#fee2e2', color: '#dc2626' },
};

const EMPTY_FORM = {
  company_name:    '',
  company_address: '',
  start_date:      '',
  end_date:        '',
};

export default function PlacementPage() {
  const [placement, setPlacement]   = useState(null);
  const [loading, setLoading]       = useState(true);
  const [showForm, setShowForm]     = useState(false);
  const [form, setForm]             = useState(EMPTY_FORM);
  const [letterFile, setLetterFile] = useState(null);
  const [uploading, setUploading]   = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError]           = useState('');
  const [success, setSuccess]       = useState('');

  useEffect(() => { fetchPlacement(); }, []);

  const fetchPlacement = async () => {
    try {
      setLoading(true);
      const res = await API.get('/placements/my-placement/');

      // Backend returns a list — extract the first item
      const data = res.data;
      const list = Array.isArray(data) ? data : data.results ?? [];
      setPlacement(list.length > 0 ? list[0] : null);
    } catch {
      setPlacement(null);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) =>
    setForm((f) => ({ ...f, [e.target.name]: e.target.value }));

  // ── Submit new placement request ─────────────────────────────
  const handleSubmitRequest = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');
    setSuccess('');

    try {
      // Step 1: create the placement record
      const res = await API.post('/placements/my-placement/', form);
      const newPlacement = res.data;

      // Step 2: if a letter was selected, upload it immediately
      if (letterFile) {
        const fd = new FormData();
        fd.append('acceptance_letter', letterFile);
        try {
          const uploadRes = await API.patch(
            `/placements/${newPlacement.id}/upload-letter/`,
            fd,
            { headers: { 'Content-Type': 'multipart/form-data' } }
          );
          setPlacement(uploadRes.data);
        } catch {
          // Placement created but letter failed — still show placement
          setPlacement(newPlacement);
          setError('Placement submitted but letter upload failed. You can upload it below.');
        }
      } else {
        setPlacement(newPlacement);
      }

      setShowForm(false);
      setForm(EMPTY_FORM);
      setLetterFile(null);
      if (!error) {
        setSuccess('Placement request submitted! Waiting for administrator approval.');
      }
    } catch (err) {
      const data = err.response?.data;
      setError(
        typeof data === 'object'
          ? Object.values(data).flat().join(' ')
          : 'Failed to submit request.'
      );
    } finally {
      setSubmitting(false);
    }
  };

  // ── Upload letter to existing placement ──────────────────────
  const handleUploadLetter = async () => {
    if (!letterFile || !placement) return;
    setUploading(true);
    setError('');
    setSuccess('');

    try {
      const fd = new FormData();
      fd.append('acceptance_letter', letterFile);
      const res = await API.patch(
        `/placements/${placement.id}/upload-letter/`,
        fd,
        { headers: { 'Content-Type': 'multipart/form-data' } }
      );
      setPlacement(res.data);
      setLetterFile(null);
      setSuccess('Acceptance letter uploaded successfully!');
    } catch (err) {
      console.error('Upload error:', err.response?.status, err.response?.data);
      setError('Failed to upload letter. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  if (loading) return <p style={{ padding: 32, color: '#64748b' }}>Loading placement…</p>;

  return (
    <div>
      <h1 className="page-title">My Internship Placement</h1>

      {success && (
        <div style={{ background: '#dcfce7', color: '#16a34a', padding: '10px 16px', borderRadius: 8, marginBottom: 16, fontSize: 14 }}>
          ✓ {success}
        </div>
      )}

      {error && (
        <div style={{ background: '#fee2e2', color: '#dc2626', padding: '10px 16px', borderRadius: 8, marginBottom: 16, fontSize: 14 }}>
          {error}
        </div>
      )}

      {/* ── No placement yet ── */}
      {!placement && !showForm && (
        <div className="card" style={{ textAlign: 'center', padding: 40 }}>
          <div style={{ fontSize: 48, marginBottom: 16 }}>📋</div>
          <h3 style={{ marginBottom: 8, fontWeight: 700 }}>No Placement Yet</h3>
          <p style={{ color: '#64748b', marginBottom: 24 }}>
            Submit a placement request with your acceptance letter to get started.
          </p>
          <button className="btn btn-primary" onClick={() => setShowForm(true)}>
            + Submit Placement Request
          </button>
        </div>
      )}

      {/* ── Request form ── */}
      {showForm && (
        <div className="card" style={{ borderLeft: '4px solid #1a56db' }}>
          <h3 style={{ marginBottom: 20, fontWeight: 700 }}>New Placement Request</h3>
          <form onSubmit={handleSubmitRequest}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
              <div className="form-group" style={{ gridColumn: '1 / -1' }}>
                <label>Company / Organisation Name</label>
                <input
                  className="form-control"
                  name="company_name" value={form.company_name}
                  onChange={handleChange}
                  placeholder="e.g. Stanbic Bank Uganda" required
                />
              </div>
              <div className="form-group" style={{ gridColumn: '1 / -1' }}>
                <label>Company Address</label>
                <textarea
                  className="form-control"
                  name="company_address" value={form.company_address}
                  onChange={handleChange} rows={2}
                  placeholder="Full address of the company" required
                />
              </div>
              <div className="form-group">
                <label>Start Date</label>
                <input
                  className="form-control"
                  type="date" name="start_date" value={form.start_date}
                  onChange={handleChange} required
                />
              </div>
              <div className="form-group">
                <label>End Date</label>
                <input
                  className="form-control"
                  type="date" name="end_date" value={form.end_date}
                  onChange={handleChange} required
                />
              </div>
            </div>

            <div className="form-group">
              <label>
                Acceptance Letter{' '}
                <span style={{ color: '#94a3b8', fontWeight: 400, fontSize: 12 }}>(PDF or image — recommended)</span>
              </label>
              <input
                type="file" accept=".pdf,.jpg,.jpeg,.png"
                className="form-control"
                onChange={(e) => setLetterFile(e.target.files[0])}
                style={{ padding: '8px 12px' }}
              />
              {letterFile && (
                <p style={{ fontSize: 13, color: '#16a34a', marginTop: 4 }}>
                  ✓ {letterFile.name} selected
                </p>
              )}
            </div>

            <div style={{ display: 'flex', gap: 10 }}>
              <button type="submit" className="btn btn-primary" disabled={submitting}>
                {submitting ? 'Submitting…' : 'Submit Request'}
              </button>
              <button
                type="button" className="btn btn-outline"
                onClick={() => { setShowForm(false); setError(''); }}
                disabled={submitting}
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* ── Existing placement details ── */}
      {placement && (
        <>
          <div style={{
            padding: '12px 20px', borderRadius: 10, marginBottom: 20,
            display: 'flex', alignItems: 'center', gap: 12,
            ...(STATUS_COLORS[placement.status] || STATUS_COLORS.pending)
          }}>
            <span style={{ fontSize: 20 }}>
              {placement.status === 'active'    ? '✅' :
               placement.status === 'pending'   ? '⏳' :
               placement.status === 'completed' ? '🎓' : '❌'}
            </span>
            <div>
              <strong style={{ textTransform: 'capitalize' }}>{placement.status}</strong>
              {placement.status === 'pending' && (
                <span style={{ marginLeft: 8, fontSize: 13 }}>— Awaiting administrator approval</span>
              )}
              {placement.status === 'active' && (
                <span style={{ marginLeft: 8, fontSize: 13 }}>— Your placement has been approved</span>
              )}
              {placement.status === 'cancelled' && (
                <span style={{ marginLeft: 8, fontSize: 13 }}>— Your placement was rejected. Contact your administrator.</span>
              )}
            </div>
          </div>

          <div className="card" style={{ marginBottom: 20 }}>
            <h3 style={{ marginBottom: 16, fontWeight: 700 }}>Placement Details</h3>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
              {[
                ['Company',              placement.company_name],
                ['Status',               placement.status],
                ['Start Date',           placement.start_date],
                ['End Date',             placement.end_date],
                ['Workplace Supervisor', placement.workplace_supervisor_name || '—'],
                ['Academic Supervisor',  placement.academic_supervisor_name  || '—'],
              ].map(([label, value]) => (
                <div key={label}>
                  <div style={{ fontSize: 12, fontWeight: 700, color: '#64748b', textTransform: 'uppercase', marginBottom: 4 }}>
                    {label}
                  </div>
                  <div style={{ fontWeight: 500 }}>{value || '—'}</div>
                </div>
              ))}
              <div style={{ gridColumn: '1 / -1' }}>
                <div style={{ fontSize: 12, fontWeight: 700, color: '#64748b', textTransform: 'uppercase', marginBottom: 4 }}>
                  Company Address
                </div>
                <div style={{ fontWeight: 500 }}>{placement.company_address || '—'}</div>
              </div>
            </div>
          </div>

          <div className="card">
            <h3 style={{ marginBottom: 16, fontWeight: 700 }}>Acceptance Letter</h3>
            {placement.acceptance_letter ? (
              <div style={{ display: 'flex', alignItems: 'center', gap: 16, flexWrap: 'wrap' }}>
                <div style={{ background: '#f1f5f9', padding: '10px 16px', borderRadius: 8, fontSize: 14, color: '#475569' }}>
                  📄 Letter uploaded {placement.letter_submitted_at
                    ? `on ${new Date(placement.letter_submitted_at).toLocaleDateString()}`
                    : ''}
                </div>
                <a
                  href={`http://localhost:8000${placement.acceptance_letter}`}
                  target="_blank" rel="noreferrer"
                  className="btn btn-outline"
                  style={{ fontSize: 13 }}
                >
                  View Letter
                </a>
                {placement.status === 'pending' && (
                  <label style={{ cursor: 'pointer' }}>
                    <span className="btn btn-outline" style={{ fontSize: 13 }}>Replace Letter</span>
                    <input
                      type="file" accept=".pdf,.jpg,.jpeg,.png" style={{ display: 'none' }}
                      onChange={(e) => setLetterFile(e.target.files[0])}
                    />
                  </label>
                )}
              </div>
            ) : (
              <div>
                <p style={{ color: '#64748b', marginBottom: 12, fontSize: 14 }}>
                  No acceptance letter uploaded yet. Upload one so the administrator can review and approve your placement.
                </p>
                <div style={{ display: 'flex', alignItems: 'center', gap: 12, flexWrap: 'wrap' }}>
                  <input
                    type="file" accept=".pdf,.jpg,.jpeg,.png"
                    onChange={(e) => setLetterFile(e.target.files[0])}
                    style={{ fontSize: 14 }}
                  />
                  {letterFile && (
                    <button className="btn btn-primary" onClick={handleUploadLetter} disabled={uploading}>
                      {uploading ? 'Uploading…' : 'Upload Letter'}
                    </button>
                  )}
                </div>
                {letterFile && (
                  <p style={{ fontSize: 13, color: '#16a34a', marginTop: 6 }}>
                    ✓ {letterFile.name} ready to upload
                  </p>
                )}
              </div>
            )}

            {letterFile && placement.acceptance_letter && placement.status === 'pending' && (
              <div style={{ marginTop: 12, display: 'flex', alignItems: 'center', gap: 10 }}>
                <span style={{ fontSize: 13, color: '#475569' }}>New file: {letterFile.name}</span>
                <button className="btn btn-primary" style={{ fontSize: 13 }} onClick={handleUploadLetter} disabled={uploading}>
                  {uploading ? 'Uploading…' : 'Confirm Upload'}
                </button>
                <button className="btn btn-outline" style={{ fontSize: 13 }} onClick={() => setLetterFile(null)}>
                  Cancel
                </button>
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
}