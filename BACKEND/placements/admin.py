from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import InternshipPlacement
# Register your models here.

class InternshipPlacementAdmin(admin.ModelAdmin):
    list_display = ('student', 'company_name', 'start_date', 'end_date','status')
    list_filter= ('status','start_date')
    search_fields = ('student_username', 'company_name')

admin.site.register(InternshipPlacement, InternshipPlacementAdmin)