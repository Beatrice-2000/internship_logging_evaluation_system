import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute   from './Components/auth/ProtectedRoute';
import MainLayout       from './components/layout/MainLayout';

// Public
import LoginPage        from './pages/LoginPage';
import UnauthorizedPage from './pages/UnauthorizedPage';

// Student
import StudentDashboard from './pages/student/StudentDashboard';
import LogbookPage      from './pages/student/LogbookPage';
import PlacementPage    from './pages/student/PlacementPage';
import EvaluationPage   from './pages/student/EvaluationPage';

// Supervisor
import SupervisorDashboard from './pages/supervisor/SupervisorDashboard';
import SupervisorReviews   from './pages/supervisor/SupervisorReviews';

// Academic
import AcademicDashboard from './pages/academic/AcademicDashboard';

// Admin
import AdminDashboard from './pages/admin/AdminDashboard';

import './styles/index.css';

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>

          {/* ── Public ── */}
          <Route path="/"             element={<Navigate to="/login" replace />} />
          <Route path="/login"        element={<LoginPage />} />
          <Route path="/unauthorized" element={<UnauthorizedPage />} />

          {/* ── Student ── */}
          <Route path="/student" element={
            <ProtectedRoute roles={['student']}><MainLayout /></ProtectedRoute>
          }>
            <Route index             element={<Navigate to="dashboard" replace />} />
            <Route path="dashboard"  element={<StudentDashboard />} />
            <Route path="logbook"    element={<LogbookPage />} />
            <Route path="placement"  element={<PlacementPage />} />
            <Route path="evaluation" element={<EvaluationPage />} />
          </Route>

          {/* ── Workplace Supervisor ── */}
          <Route path="/supervisor" element={
            <ProtectedRoute roles={['workplace_supervisor']}><MainLayout /></ProtectedRoute>
          }>
            <Route index            element={<Navigate to="dashboard" replace />} />
            <Route path="dashboard" element={<SupervisorDashboard />} />
            <Route path="reviews"   element={<SupervisorReviews />} />
          </Route>

          {/* ── Academic Supervisor ── */}
          <Route path="/academic" element={
            <ProtectedRoute roles={['academic_supervisor']}><MainLayout /></ProtectedRoute>
          }>
            <Route index              element={<Navigate to="dashboard" replace />} />
            <Route path="dashboard"   element={<AcademicDashboard />} />
            <Route path="evaluations" element={<div style={{padding:28}}><h1 className="page-title">Evaluations — Week 9</h1></div>} />
          </Route>

          {/* ── Administrator ── */}
          <Route path="/admin" element={
            <ProtectedRoute roles={['administrator']}><MainLayout /></ProtectedRoute>
          }>
            <Route index             element={<Navigate to="dashboard" replace />} />
            <Route path="dashboard"  element={<AdminDashboard />} />
            <Route path="users"      element={<div style={{padding:28}}><h1 className="page-title">User Management — Week 4</h1></div>} />
            <Route path="placements" element={<div style={{padding:28}}><h1 className="page-title">Placements — Week 5</h1></div>} />
            <Route path="reports"    element={<div style={{padding:28}}><h1 className="page-title">Reports — Week 10</h1></div>} />
          </Route>

          {/* Catch-all */}
          <Route path="*" element={<Navigate to="/login" replace />} />

        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

