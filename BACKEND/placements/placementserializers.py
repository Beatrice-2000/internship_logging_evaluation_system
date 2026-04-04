from rest_framework import serializers
from .models import InternshipPlacement

class InternshipPlacementSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source= 'student.username', read_only = True)
    class Meta:
        model= InternshipPlacement
        fields = [
            'id', 'student','student_name',
            'workplace_supervisor','organization',
            'project_title','start_date','end_date',
            'created_at','status']
        read_only_field= ['created_at']

        def validate(self, data):
            start = data.get('start_date')
            end = data.get('end_date')
            if start and end and start > end:
                raise serializers.ValidationError("Invalid start date")
            return data