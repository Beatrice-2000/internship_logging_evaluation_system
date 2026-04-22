from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import WeeklyLog, SupervisorReview
from .serializers import WeeklyLogSerializer, SupervisorReviewSerializer

class IsOwnerOrSupervisor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return (obj.student == request.user or
                    request.user.role in ['academic_supervisor', 'workplace_supervisor', 'admin'])
        return obj.student == request.user or request.user.role == 'admin'

class IsSupervisorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                request.user.role in ['academic_supervisor', 'workplace_supervisor', 'admin'])

class WeeklyLogListCreateView(generics.ListCreateAPIView):
    serializer_class = WeeklyLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return WeeklyLog.objects.all()
        elif user.role in ['academic_supervisor', 'workplace_supervisor']:
            return (WeeklyLog.objects.filter(placement__academic_supervisor=user) |
                    WeeklyLog.objects.filter(placement__workplace_supervisor=user))
        elif user.role == 'student':
            return WeeklyLog.objects.filter(student=user)
        return WeeklyLog.objects.none()

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

class WeeklyLogDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WeeklyLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSupervisor]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'academic_supervisor', 'workplace_supervisor']:
            return WeeklyLog.objects.all()
        return WeeklyLog.objects.filter(student=user)

class SubmitLogView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            log = WeeklyLog.objects.get(pk=pk, student=request.user)
        except WeeklyLog.DoesNotExist:
            return Response(
                {'error': 'Log not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        if log.status != 'draft':
            return Response(
                {'error': 'Only draft logs can be submitted.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        log.status = 'submitted'
        log.submitted_at = timezone.now()
        log.save()
        return Response(
            {'message': 'Log submitted successfully!'},
            status=status.HTTP_200_OK
        )

class SupervisorReviewView(generics.CreateAPIView):
    serializer_class = SupervisorReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsSupervisorOrAdmin]

    def perform_create(self, serializer):
        log_id = self.kwargs.get('log_id')
        log = WeeklyLog.objects.get(pk=log_id)
        serializer.save(supervisor=self.request.user, log=log)
        log.status = 'reviewed'
        log.save()

class StudentLogbookView(generics.ListCreateAPIView):
    serializer_class = WeeklyLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role=='student':
            return WeeklyLog.objects/filter(students= self.request.user)
        return WeeklyLog.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(student= self.request.user)