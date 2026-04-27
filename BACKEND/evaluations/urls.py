from django.urls import path
from . import views

urlpatterns = [
    # Evaluation Criteria
    path('criteria/', views.EvaluationCriteriaListView.as_view(), name='criteria-list'),
    path('criteria/<int:pk>/', views.EvaluationCriteriaDetailView.as_view(), name='criteria-detail'),

    # Main Evaluations
    path('', views.EvaluationListCreateView.as_view(), name='evaluation-list-create'),
    path('<int:pk>/', views.EvaluationDetailView.as_view(), name='evaluation-detail'),

    # Student Views
    path('student/', views.StudentEvaluationView.as_view(), name='student-evaluations'),
    path('score/<int:student_id>/', views.StudentScoreView.as_view(), name='student-score'),

    # Academic Evaluations
    path('academic/', views.AcademicEvaluationListCreateView.as_view(), name='academic-evaluation-list-create'),
    path('academic/<int:pk>/', views.AcademicEvaluationDetailView.as_view(), name='academic-evaluation-detail'),

    # Admin Report
    path('admin-report/', views.AdminReportView.as_view(), name='admin-report'),
]