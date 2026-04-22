from django.urls import path
from . import views

urlpatterns = [
    path('', views.WeeklyLogListCreateView.as_view(), name='log-list-create'),
    path('<int:pk>/', views.WeeklyLogDetailView.as_view(), name='log-detail'),
    path('<int:pk>/submit/', views.SubmitLogView.as_view(), name='log-submit'),
    path('<int:log_id>/review/', views.SupervisorReviewView.as_view(), name='log-review'),
]