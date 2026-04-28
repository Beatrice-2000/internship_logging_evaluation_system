import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { AuthContext } from './context/AuthContext';
import { useContext, lazy, Suspense, useMemo } from 'react';
import MainLayout from './Components/layout/MainLayout';

// Public (eager load for critical paths)
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import UnauthorizedPage from './pages/UnauthorizedPage';
import NotFoundPage from './pages/NotFoundPage';

// Lazy load protected pages for better performance
const StudentDashboard = lazy(() => import('./pages/student/StudentDashboard'));
const LogbookPage = lazy(() => import('./pages/student/LogbookPage'));
const EvaluationPage = lazy(() => import('./pages/student/EvaluationPage'));
const PlacementPage = lazy(() => import('./pages/student/PlacementPage'));
const ScoreResultsPage = lazy(() => import('./pages/student/ScoreResultsPage'));

const SupervisorDashboard = lazy(() => import('./pages/supervisor/SupervisorDashboard'));
const SupervisorReviews = lazy(() => import('./pages/supervisor/SupervisorReviews'));
const LogbookDetailPage = lazy(() => import('./pages/supervisor/LogbookDetailPage'));

const AcademicDashboard = lazy(() => import('./pages/academic/AcademicDashboard'));
const AcademicEvaluationPage = lazy(() => import('./pages/academic/AcademicEvaluationPage'));

const AdminDashboard = lazy(() => import('./pages/admin/AdminDashboard'));
const UserManagementPage = lazy(() => import('./pages/admin/UserManagementPage'));
const PlacementManagementPage = lazy(() => import('./pages/admin/PlacementManagementPage'));
const AdminStatisticsPage = lazy(() => import('./pages/admin/AdminStatisticsPage'));

// Loading component for Suspense fallback
const LoadingSpinner = () => (
  <div className="flex items-center justify-center min-h-screen">
    <div className="text-center">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
      <p className="mt-4 text-gray-600">Loading...</p>
    </div>
  </div>
);

// Enhanced ProtectedRoute component
const ProtectedRoute = ({ children, allowedRoles }) => {
  const { user, loading } = useContext(AuthContext);
  
  if (loading) return <LoadingSpinner />;
  if (!user) return <Navigate to="/login" replace />;
  if (allowedRoles && !allowedRoles.includes(user.role)) {
    return <Navigate to="/unauthorized" replace />;
  }
  return children;
};

// Role to base path mapping
const ROLE_BASE_PATHS = {
  student: '/student',
  supervisor: '/supervisor',
  academic: '/academic',
  admin: '/admin'
};

// Route wrapper with layout
const ProtectedLayoutRoute = ({ roles, children }) => (
  <ProtectedRoute allowedRoles={roles}>
    <MainLayout>{children}</MainLayout>
  </ProtectedRoute>
);

export default function App() {
  // Get user from context for default redirect
  const { user, loading } = useContext(AuthContext);
  
  // Memoize default path to avoid recalculation
  const defaultPath = useMemo(() => {
    if (!user) return '/login';
    return ROLE_BASE_PATHS[user.role] || '/login';
  }, [user]);
  
  if (loading) return <LoadingSpinner />;

  return (
    <BrowserRouter>
      <AuthProvider>
        <Suspense fallback={<LoadingSpinner />}>
          <Routes>
            {/* ── Public Routes ── */}
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/unauthorized" element={<UnauthorizedPage />} />
            
            {/* Root redirect based on user role */}
            <Route path="/" element={<Navigate to={defaultPath} replace />} />

            {/* ── Student Routes ── */}
            <Route 
              path="/student" 
              element={
                <ProtectedRoute allowedRoles={['student']}>
                  <MainLayout />
                </ProtectedRoute>
              }
            >
              <Route index element={<Navigate to="dashboard" replace />} />
              <Route path="dashboard" element={<StudentDashboard />} />
              <Route path="logbook" element={<LogbookPage />} />
              <Route path="placement" element={<PlacementPage />} />
              <Route path="evaluation" element={<EvaluationPage />} />
              <Route path="scores" element={<ScoreResultsPage />} />
            </Route>

            {/* ── Workplace Supervisor Routes ── */}
            <Route 
              path="/supervisor" 
              element={
                <ProtectedRoute allowedRoles={['supervisor', 'workplace_supervisor']}>
                  <MainLayout />
                </ProtectedRoute>
              }
            >
              <Route index element={<Navigate to="dashboard" replace />} />
              <Route path="dashboard" element={<SupervisorDashboard />} />
              <Route path="reviews" element={<SupervisorReviews />} />
              <Route path="reviews/:logId" element={<LogbookDetailPage />} />
            </Route>

            {/* ── Academic Supervisor Routes ── */}
            <Route 
              path="/academic" 
              element={
                <ProtectedRoute allowedRoles={['academic', 'academic_supervisor']}>
                  <MainLayout />
                </ProtectedRoute>
              }
            >
              <Route index element={<Navigate to="dashboard" replace />} />
              <Route path="dashboard" element={<AcademicDashboard />} />
              <Route path="evaluate" element={<AcademicEvaluationPage />} />
              <Route path="scores" element={<ScoreResultsPage />} />
            </Route>

            {/* ── Administrator Routes ── */}
            <Route 
              path="/admin" 
              element={
                <ProtectedRoute allowedRoles={['admin', 'administrator']}>
                  <MainLayout />
                </ProtectedRoute>
              }
            >
              <Route index element={<Navigate to="dashboard" replace />} />
              <Route path="dashboard" element={<AdminDashboard />} />
              <Route path="users" element={<UserManagementPage />} />
              <Route path="placements" element={<PlacementManagementPage />} />
              <Route path="statistics" element={<AdminStatisticsPage />} />
              <Route path="reports" element={<AdminStatisticsPage />} />
            </Route>

            {/* ── 404 Catch-all ── */}
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </Suspense>
      </AuthProvider>
    </BrowserRouter>
  );
}