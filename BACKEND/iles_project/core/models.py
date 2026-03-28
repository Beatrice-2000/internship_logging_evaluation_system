from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

# ---------------------
# User Model
# ---------------------
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student Intern'),
        ('workplace_supervisor', 'Workplace Supervisor'),
        ('academic_supervisor', 'Academic Supervisor'),
        ('admin', 'Internship Administrator'),
    ]
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"


# ---------------------
# Internship Placement
# ---------------------
class InternshipPlacement(models.Model):
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'}
    )

    workplace_supervisor = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='workplace_supervisions',
        limit_choices_to={'role': 'workplace_supervisor'}
    )

    academic_supervisor = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='academic_supervisions',
        limit_choices_to={'role': 'academic_supervisor'}
    )

    organization = models.CharField(max_length=255)
    project_title = models.CharField(max_length=255)

    start_date = models.DateField()
    end_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Validate start < end
        if self.start_date > self.end_date:
            raise ValidationError("Start date cannot be after end date.")

        # Prevent overlapping placements
        overlapping = InternshipPlacement.objects.filter(
            student=self.student,
            start_date__lte=self.end_date,
            end_date__gte=self.start_date
        ).exclude(id=self.id)

        if overlapping.exists():
            raise ValidationError(
                "Student already has an internship during this period."
            )

    def __str__(self):
        return f"{self.student.username} - {self.organization}"


# ---------------------
# Weekly Log
# ---------------------
class WeeklyLog(models.Model):
    placement = models.ForeignKey(
        InternshipPlacement,
        on_delete=models.CASCADE,
        related_name='logs'
    )
    week_number = models.IntegerField()
    work_done = models.TextField()
    challenges = models.TextField(blank=True)
    submission_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('placement', 'week_number')

    def __str__(self):
        return f"Week {self.week_number} - {self.placement.student.username}"


# ---------------------
# Supervisor Review
# ---------------------
class SupervisorReview(models.Model):
    log = models.OneToOneField(WeeklyLog, 
                               on_delete=models.CASCADE,
                               related_name= 'review')
    supervisor = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role__in': ['workplace_supervisor', 'academic_supervisor']}
    )
    comments = models.TextField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Review for {self.log}"


# ---------------------
# Academic Evaluation
# ---------------------
class AcademicEvaluation(models.Model):
    placement = models.OneToOneField(InternshipPlacement, on_delete=models.CASCADE)
    academic_supervisor = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': 'academic_supervisor'}
    )
    score = models.FloatField()
    feedback = models.TextField()

    def __str__(self):
        return f"Evaluation - {self.placement.student.username}"