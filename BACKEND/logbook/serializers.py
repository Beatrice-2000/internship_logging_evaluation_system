from rest_framework import serializers
from .models import WeeklyLog, SupervisorReview

class SupervisorReviewSerializer(serializers.ModelSerializer):
    supervisor_name = serializers.CharField(source='supervisor.username', read_only=True)

    class Meta:
        model = SupervisorReview
        fields = ['id', 'log', 'supervisor',
                  'supervisor_name', 'comments', 'approved']
        read_only_fields = ['supervisor']

class WeeklyLogSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.username', read_only=True)
    review = SupervisorReviewSerializer(read_only=True)

    class Meta:
        model = WeeklyLog
        fields = ['id', 'placement', 'student', 'student_name',
                  'week_number', 'activities', 'skills_learned',
                  'challenges', 'status', 'submitted_at',
                  'created_at', 'updated_at', 'review']
        read_only_fields = ['student', 'submitted_at', 'created_at', 'updated_at']

    def validate(self, data):
        if data.get('status') == 'submitted':
            if not data.get('activities'):
                raise serializers.ValidationError(
                    "Activities field is required before submitting."
                )
        return data