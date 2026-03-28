from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Evaluation, EvaluationCriteria
# Register your models here.

admin.site.register(Evaluation)
admin.site.register(EvaluationCriteria)