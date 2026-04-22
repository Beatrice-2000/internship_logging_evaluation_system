from django.urls import path
from . import views

urlpatterns = [
    path('criteria/', views.EvaluationCriteriaListView.as_view(), name='criteria-list'),
    path('', views.EvaluationListCreateView.as_view(), name='evaluation-list-create'),
    path('<int:pk>/', views.EvaluationDetailView.as_view(), name='evaluation-detail'),
    #path('academic/', views.AcademicEvaluationListCreateView.as_view(), name='academic-evaluation'),
    #path('score/<int:student_id>/', views.StudentScoreView.as_view(), name='student-score'),
]