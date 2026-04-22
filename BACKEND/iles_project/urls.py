from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import RegisterView, LoginView, LogoutView, AdminUserListView
from evaluations.views import AdminReportView
from logbook.views import StudentLogbookView


urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Users
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/users/', include('users.urls')),

    # Placements
    path('api/placements/', include('placements.urls')),

    # Logbook
    path('api/logs/', include('logbook.urls')),

    # Evaluations
    path('api/evaluations/', include('evaluations.urls')),

    #Frontend auth endpoints
    path('api/auth/login/', LoginView.as_view(), name='auth-login'),
    path('api/auth/register/', RegisterView.as_view(), name= 'auth-register'),
    path('api/auth/logout/', LogoutView.as_view(), name='auth-logout'),
    
    #Admin endpoints
    path('api/admin/users/', AdminUserListView.as_view(), name='admin-users'),#users
    path('api/admin/reports/', AdminReportView.as_view(), name= 'admin-reports'),

    #Student logbook endpoints
    path('api/student/logbook/', StudentLogbookView.as_view(), name='student-logbook'),



]