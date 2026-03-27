from rest_framework import serializers
from .models import User, InternshipPlacement, WeeklyLog, SupervisorReview, AcademicEvaluation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'first_name', 'last_name']


class InternshipPlacementSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.username', read_only=True)

    class Meta:
        model = InternshipPlacement
        fields = [
            'id',
            'student', 'student_name',
            'workplace_supervisor',
            'academic_supervisor',
            'organization',
            'project_title',
            'start_date',
            'end_date',
            'created_at'
        ]
        read_only_fields = ['created_at']

    def validate(self, data):
        start = data.get('start_date')
        end = data.get('end_date')
        if start and end and start > end:
            raise serializers.ValidationError("Start date cannot be after end date.")
        return data


class WeeklyLogSerializer(serializers.ModelSerializer):
    student = serializers.CharField(source='placement.student.username', read_only=True)

    class Meta:
        model = WeeklyLog
        fields = ['id', 'placement', 'student', 'week_number', 'work_done', 'challenges', 'submission_date']
        read_only_fields = ['submission_date']


class SupervisorReviewSerializer(serializers.ModelSerializer):
    supervisor_name = serializers.CharField(source='supervisor.username', read_only=True)

    class Meta:
        model = SupervisorReview
        fields = ['id', 'log', 'supervisor', 'supervisor_name', 'comments', 'approved']


class AcademicEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicEvaluation
        fields = ['id', 'placement', 'academic_supervisor', 'score', 'feedback']