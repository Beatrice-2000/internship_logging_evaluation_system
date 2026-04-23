from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import InternshipPlacement
from .serializers import InternshipPlacementSerializer

class IsAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.role == 'admin')

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return (request.user.is_authenticated and 
                request.user.role == 'admin')

class PlacementListCreateView(generics.ListCreateAPIView):
    serializer_class = InternshipPlacementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return InternshipPlacement.objects.all()
        elif user.role == 'academic_supervisor':
            return InternshipPlacement.objects.filter(
                academic_supervisor=user
            )
        elif user.role == 'workplace_supervisor':
            return InternshipPlacement.objects.filter(
                workplace_supervisor=user
            )
        elif user.role == 'student':
            return InternshipPlacement.objects.filter(
                student=user
            )
        return InternshipPlacement.objects.none()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsAdminOnly()]
        return [permissions.IsAuthenticated()]

class PlacementDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InternshipPlacementSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return InternshipPlacement.objects.all()
        elif user.role == 'academic_supervisor':
            return InternshipPlacement.objects.filter(
                academic_supervisor=user
            )
        elif user.role == 'workplace_supervisor':
            return InternshipPlacement.objects.filter(
                workplace_supervisor=user
            )
        elif user.role == 'student':
            return InternshipPlacement.objects.filter(
                student=user
            )
        return InternshipPlacement.objects.none()

class PlacementStatusUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminOnly]

    def patch(self, request, pk):
        try:
            placement = InternshipPlacement.objects.get(pk=pk)
        except InternshipPlacement.DoesNotExist:
            return Response(
                {'error': 'Placement not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        new_status = request.data.get('status')
        valid_statuses = ['pending', 'active', 'completed', 'cancelled']
        if new_status not in valid_statuses:
            return Response(
                {'error': f'Invalid status. Choose from {valid_statuses}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        placement.status = new_status
        placement.save()
        return Response(
            {'message': f'Placement status updated to {new_status}!'},
            status=status.HTTP_200_OK
        )
    
class AdminPlacementListView(generics.ListAPIView):
    serializer_class = InternshipPlacementSerializer
    permission_classes= [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role=='admin':
            return InternshipPlacement.objects.all()
        return InternshipPlacement.objects.none()
    
class StudentPlacementView(generics.ListAPIView):
    serializer_class = InternshipPlacementSerializer
    permission_classes = [permissions.IsAuthenticated]