from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, LoginView, LogoutView,
    ProfileView, ChangePasswordView,
    AdminUserListView, AdminUserDetailView,
    AdminUserActivateView, UsersByRoleView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', AdminUserListView.as_view(), name='user-list'),
    path('<int:pk>/', AdminUserDetailView.as_view(), name='user-detail'),
    path('<int:pk>/activate/', AdminUserActivateView.as_view(), name='user-activate'),
    path('by-role/', UsersByRoleView.as_view(), name='users-by-role'),
]