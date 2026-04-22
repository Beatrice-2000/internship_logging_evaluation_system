from rest_framework import serializers
from .models import InternshipPlacement

class InternshipPlacementSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.username', read_only=True)
    workplace_supervisor_name = serializers.CharField(source='workplace_supervisor.username', read_only=True)
    academic_supervisor_name = serializers.CharField(source='academic_supervisor.username', read_only=True)

    class Meta:
        model = InternshipPlacement
        fields = '__all__'
        read_only_fields = ['created_at']

    def validate(self, data):
        if data.get('start_date') and data.get('end_date'):
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError("Start date cannot be after end date.")
        return data