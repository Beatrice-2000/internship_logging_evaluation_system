from rest_framework import serializers
from .models import Evaluation, EvaluationCriteria, AcademicEvaluation

class EvaluationCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationCriteria
        fields = '__all__'

class EvaluationSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.username', read_only=True)
    evaluator_name = serializers.CharField(source='evaluator.username', read_only=True)
    criteria_name = serializers.CharField(source='criteria.name', read_only=True)
    criteria_weight = serializers.DecimalField(
        source='criteria.weight',
        max_digits=5,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Evaluation
        fields = '__all__'
        read_only_fields = ['evaluator', 'evaluated_at']

    def validate_score(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Score must be between 0 and 100.")
        return value

class AcademicEvaluationSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(
        source='placement.student.username',
        read_only=True
    )
    supervisor_name = serializers.CharField(
        source='academic_supervisor.username',
        read_only=True
    )

    class Meta:
        model = AcademicEvaluation
        fields = '__all__'
        read_only_fields = ['academic_supervisor']

    def validate_score(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Score must be between 0 and 100.")
        return value