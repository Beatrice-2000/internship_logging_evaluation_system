from rest_framework import generics, permissions
from .models import Evaluation, EvaluationCriteria
from .serializers import EvaluationSerializer, EvaluationCriteriaSerializer

class IsSupervisorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.role in ['academic_supervisor', 'workplace_supervisor', 'admin'])

class EvaluationListCreateView(generics.ListCreateAPIView):
    serializer_class = EvaluationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Evaluation.objects.all()
        elif user.role in ['academic_supervisor', 'workplace_supervisor']:
            return Evaluation.objects.filter(evaluator=user)
        elif user.role == 'student':
            return Evaluation.objects.filter(placement__student=user)
        return Evaluation.objects.none()

class EvaluationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EvaluationSerializer
    permission_classes = [permissions.IsAuthenticated, IsSupervisorOrAdmin]

    def get_queryset(self):
        return Evaluation.objects.all()

class EvaluationCriteriaListView(generics.ListCreateAPIView):
    serializer_class = EvaluationCriteriaSerializer
    permission_classes = [permissions.IsAuthenticated, IsSupervisorOrAdmin]
    queryset = EvaluationCriteria.objects.filter(is_active=True)