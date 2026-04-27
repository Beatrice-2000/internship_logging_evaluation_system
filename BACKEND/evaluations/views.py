from rest_framework import generics, permissions
from .models import Evaluation, EvaluationCriteria, AcademicEvaluation
from .serializers import EvaluationSerializer, EvaluationCriteriaSerializer, AcademicEvaluationSerializer
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
        total_logs = WeeklyLog.objects.count()
        active_placements = InternshipPlacement.objects.filter(status ='active').count()
        pending_reviews = WeeklyLog.objects.filter(status='submitted').count()

        total_scores =[]
        students = CustomUser.objects.filter(role= 'student')

        for student in students:
            evaluations = Evaluation.objects.filter(student= student)
            if evaluations.exists():
                weighted_sum = 0
                for eval in evaluations:
                    weighted_sum += float(eval.criteria.weight) * float(eval.score)
                try:
                    academic = AcademicEvaluation.objects.get(placement__student= student)
                    academic_score = float(academic.score)
                except AcademicEvaluation.DoesNotExist:
                    academic_score = 0
                total_score = (weighted_sum *0.7) + (academic_score *0.3)
                total_scores.append(total_score)
        avg_score = round(sum(total_scores)/ len(total_scores), 2) if total_scores else 0
        
        data= {
            'total_students': total_students,
            'total_placements': total_placements,
            'total_logs': total_logs,
            'active_placements': active_placements,
            'pending_reviews': pending_reviews,
            'average_score' : avg_score,
        }  
        return Response(data)
    
class StudentEvaluationView(generics.ListAPIView):
    serializer_class = EvaluationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role =='student':
            return Evaluation.objects.filter(student= self.request.user)
        return Evaluation.objects.none()
    
class AcademicEvaluationListView(generics.ListAPIView):
    serializer_class = AcademicEvaluationSerializer
    permission_classes =[permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role =='academic_supervisor':
            return AcademicEvaluation.objects.filter(academic_supervisor=user)
        elif user.role=='admin':
            return AcademicEvaluation.objects.all()
        return AcademicEvaluation.objects.none()
    
class  AcademicEvaluationListCreateView(generics.ListCreateAPIView):
    serializer_class =AcademicEvaluationSerializer
    permission_classes =[permissions.IsAuthenticated]

    def get_queryset(self):
        user= self.request.user
        if user.role =='admin':
            return AcademicEvaluation.objects.all()
        elif user.role =='academic_supervisor':
            return AcademicEvaluation.objects.filter(academic_supervisor= user)
        return AcademicEvaluation.objects.none()
    
    def perform_create(self, serializer):
        if self.request.user.role != 'academic_supervisor':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only academic supervisors can create evaluations")
        
        placement_id = self.request.data.get('placement')
        try:
            placement = InternshipPlacement.objects.get(pk= placement_id)
        except InternshipPlacement.DoesNotExist:
            from rest_framework.exceptions import NotFound
            raise NotFound('Placement not found')
        
        if placement.academic_supervisor!= self.request.user:
            raise PermissionDenied("You are not the academic supervisor for this placement.")
        
        serializer.save(academic_supervisor= self.request.user)

class StudentScoreView(APIView):
    permission_classes = [permissions.IsAuthenticated]
#Check permission so only admin, academic supervisor or student can check student score
    def get(self, request, student_id):
        from users.models import CustomUser
        from .models import Evaluation, AcademicEvaluation

        user = request.user
        if user.role not in ['admin','academic_supervisor'] and user.id != student_id:
            return Response({"error":"You do not have permission to view this score!"}, status = 403)
        
        try:
            student = CustomUser.objects.get(pk= student_id, role = 'student')
        except CustomUser.DoesNotExist:
            return Response({'error':'Student Not Found'}, status= 404)
        
        evaluations = Evaluation.objects.filter(student=student)
        if not evaluations.exists():
            return Response({'total score': 0, 'grade' :'N/A', 'message':'No evaluations yet'})
        
        weighted_sum = 0
        for eval in evaluations:
            weighted_sum += float(eval.criteria.weight)* float(eval.score)

        try:
            academic= AcademicEvaluation.objects.get(placement__student= student)
            academic_score = float(academic.score)
        except AcademicEvaluation.DoesNotExist:
            academic_score = 0

#Applying weights i.e 70% for criteria sum, 30% for academic

        total_score= (weighted_sum *0.7) + (academic_score *0.3)
        total_score = round(total_score, 2)

        if total_score >=80 :
            grade = 'A'
        elif total_score >= 70:
            grade ='B'
        elif total_score >= 60:
            grade = 'C'
        elif total_score >= 50:
            grade = 'D'
        else:
            grade = 'F'

        return Response({
            'student_id': student.id,
            'student_name': student.username,
            'weighted_criteria_sum': round(weighted_sum, 2),
            'academic_evaluation_score': academic_score,
            'total_score': total_score,
            'grade': grade
        })