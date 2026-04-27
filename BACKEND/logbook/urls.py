from django.urls import path
from . import views

urlpatterns = [
    path('', views.WeeklyLogListCreateView.as_view(), name='log-list-create'),
    path('<int:pk>/', views.WeeklyLogDetailView.as_view(), name='log-detail'),
    path('<int:pk>/submit/', views.SubmitLogView.as_view(), name='log-submit'),
    path('<int:log_id>/review/', views.SupervisorReviewView.as_view(), name='log-review'),
    path('<int:log_id>/approve/', views.ApproveLogView.as_view(), name='log-approve'),
    path('review/<int:pk>/', views.SupervisorReviewDetailView.as_view(), name='review-detail'),
    path('my-logs/', views.StudentLogbookView.as_view(), name='student-logbook'),
    path('pending-reviews/', views.SupervisorReviewListView.as_view(), name='pending-reviews'),
    path('dashboard/', views.LogbookDashboardView.as_view(), name='logbook-dashboard'),
]