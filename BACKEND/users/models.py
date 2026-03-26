from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student Intern'),
        ('workplace_supervisor', 'Workplace Supervisor'),
        ('academic_supervisor', 'Academic Supervisor'),
        ('admin', 'Internship Administrator'),
    ]
    
    role = models.CharField(
        max_length=30, 
        choices=ROLE_CHOICES, 
        default='student'
    )
    phone_number = models.CharField(
        max_length=15, 
        blank=True, 
        null=True
    )
    
    def __str__(self):
        return f"{self.username} ({self.role})"
