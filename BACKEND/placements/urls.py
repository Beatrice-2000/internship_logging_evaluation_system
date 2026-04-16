from django.urls import path
from . import views

urlpatterns = [
    path('', views.PlacementListCreateView.as_view(), name='placement-list-create'),
    path('<int:pk>/', views.PlacementDetailView.as_view(), name='placement-detail'),
    path('<int:pk>/status/', views.PlacementStatusUpdateView.as_view(), name='placement-status'),
]