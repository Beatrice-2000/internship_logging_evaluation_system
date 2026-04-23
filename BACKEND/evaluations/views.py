from rest_framework import generics, permissions
from .models import Evaluation, EvaluationCriteria
from .serializers import EvaluationSerializer, EvaluationCriteriaSerializer
from placements.models import InternshipPlacement
from logbook.models import WeeklyLog
from logbook.serializers import WeeklyLogSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import CustomUser

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

class AdminReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role != 'admin':
            return Response({'error': 'Forbidden'}, status= 403)
        
        #Statistics calculations displayed to admin only
        total_students = CustomUser.objects.filter(role= 'student').count()
        total_placements = InternshipPlacement.objects.count()
        total_logs = WeeklyLog.objects.counts()
        active_placements = InternshipPlacement.objects.filter(status ='active').count()
        pending_reviews = InternshipPlacement.objects.filter(status='pending').count()

        data= {
            'total_students': total_students,
            'total_placements': total_placements,
            'total_logs': total_logs,
            'active_placements': active_placements,
            'pending_reviews': pending_reviews,
        }
        return Response(data)
    
class StudentEvaluationView(generics.ListAPIView):
    serializer_class = EvaluationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role =='student':
            return Evaluation.objects.filter(student= self.request.user)
        return Evaluation.objects.none()
    