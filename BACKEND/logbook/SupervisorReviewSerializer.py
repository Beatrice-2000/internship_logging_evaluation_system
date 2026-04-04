from rest_framework import serializers
from .models import WeeklyLog, SupervisorReview

class WeeklyLogSerializer(serializers.ModelSerializer):
    student = serializers.CharField(source= 'placement.student.username', read_only= True)
    class Meta: 
        model = WeeklyLog
        fields= ['id', 'placement','student', 'week_number','activities',
                 'challenges', 'submitted_at']
        read_only_fields=['submitted_at']

class SupervisorReviewSerializer(serializers.ModerSerializer):
    supervisor_name =serializers.CharField(source='supervisor.username', read_only= True)
    class Meta:
        model = SupervisorReview
        fields = ['id', 'log', 'supervisor',
                    'supervisor_name', 'comments','approved']