import { useNavigate } from "react-router-dom";

const NotFoundPage = () => {
  const navigate = useNavigate();

  return (
    <div style={styles.page}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Syne:wght@700;800&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        @keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-14px); } }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .btn-home:hover { background: #059669 !important; transform: translateY(-2px); }
        .btn-back:hover { border-color: #6ee7b7 !important; color: #6ee7b7 !important; }
      `}</style>

      {/* Background grid */}
      <div style={styles.bg} />

      <div style={styles.content}>
        <div style={styles.floatIcon}>🧭</div>
        <h1 style={styles.code}>404</h1>
        <h2 style={styles.title}>Page Not Found</h2>
        <p style={styles.message}>
          The page you're looking for doesn't exist or you don't have permission to view it.
        </p>
        <div style={styles.btnRow}>
          <button onClick={() => navigate(-1)} className="btn-back" style={styles.btnBack}>
            ← Go Back
          </button>
          <button onClick={() => navigate("/")} className="btn-home" style={styles.btnHome}>
            🏠 Go to Dashboard
          </button>
        </div>

        <div style={styles.linksRow}>
          <span style={styles.linksLabel}>Quick links:</span>
          {[
            { label: "Login", path: "/login" },
            { label: "Student Dashboard", path: "/student" },
            { label: "Supervisor Dashboard", path: "/supervisor" },
          ].map(({ label, path }) => (
            <button key={path} onClick={() => navigate(path)} style={styles.quickLink}>
              {label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

const styles = {
  page: {
    minHeight: "100vh",
    background: "#0f1117",
    fontFamily: "'DM Sans', sans-serif",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    position: "relative",
    overflow: "hidden",
    padding: 24,
  },
  bg: {
    position: "absolute",
    inset: 0,
    backgroundImage: "radial-gradient(circle at 20% 30%, #6ee7b715 0%, transparent 50%), radial-gradient(circle at 80% 70%, #3b82f615 0%, transparent 50%)",
    pointerEvents: "none",
  },
  content: {
    textAlign: "center",
    maxWidth: 480,
    animation: "fadeIn 0.5s ease both",
    position: "relative",
    zIndex: 1,
  },
  floatIcon: {
    fontSize: 64,
    display: "block",
    marginBottom: 16,
    animation: "float 3s ease-in-out infinite",
  },
  code: {
    fontFamily: "'Syne', sans-serif",
    fontSize: 120,
    fontWeight: 800,
    lineHeight: 1,
    background: "linear-gradient(135deg, #6ee7b7, #3b82f6)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
    backgroundClip: "text",
    marginBottom: 8,
  },
  title: {
    fontFamily: "'Syne', sans-serif",
    fontSize: 24,
    fontWeight: 700,
    color: "#f1f5f9",
    marginBottom: 12,
  },
  message: {
    fontSize: 15,
    color: "#64748b",
    lineHeight: 1.7,
    marginBottom: 36,
  },
  btnRow: {
    display: "flex",
    gap: 12,
    justifyContent: "center",
    marginBottom: 32,
    flexWrap: "wrap",
  },
  btnBack: {
    background: "transparent",
    border: "1px solid #2a2d3e",
    color: "#94a3b8",
    borderRadius: 10,
    padding: "12px 24px",
    fontSize: 14,
    cursor: "pointer",
    transition: "all 0.15s",
    fontFamily: "'DM Sans', sans-serif",
  },
  btnHome: {
    background: "#10b981",
    border: "none",
    color: "#fff",
    borderRadius: 10,
    padding: "12px 28px",
    fontSize: 14,
    fontWeight: 600,
    cursor: "pointer",
    transition: "all 0.15s",
    fontFamily: "'DM Sans', sans-serif",
  },
  linksRow: {
    display: "flex",
    alignItems: "center",
    gap: 10,
    justifyContent: "center",
    flexWrap: "wrap",
  },
  linksLabel: {
    fontSize: 12,
    color: "#475569",
  },
  quickLink: {
    background: "transparent",
    border: "none",
    color: "#6ee7b7",
    fontSize: 12,
    cursor: "pointer",
    textDecoration: "underline",
    textUnderlineOffset: 3,
    padding: 0,
    fontFamily: "'DM Sans', sans-serif",
  },
};

export default NotFoundPage;
