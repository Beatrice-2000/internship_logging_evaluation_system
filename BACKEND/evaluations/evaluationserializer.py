from rest_framework import serializers
from .models import Evaluation, EvaluationCriteria, AcademicEvaluation

class EvaluationCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationCriteria
        fields =['id', 'name', 'description',
                 'weight', 'is_active']
        
class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model= Evaluation
        fields= ['id', 'student'
               'placement','evaluator', 'criteria','score',
               'comments','evaluated_at']
    


class AcademicEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicEvaluation
        fields = ['id', 'placement', 
                  'academic_supervisor', 'score',
                    'feedback']