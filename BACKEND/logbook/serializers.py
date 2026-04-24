from rest_framework import serializers
from django.utils import timezone
from .models import WeeklyLog, SupervisorReview


class SupervisorReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for SupervisorReview model.
    Handles reviews submitted by workplace and academic supervisors.
    Each weekly log can have one review.
    """
    supervisor_name = serializers.CharField(
        source='supervisor.username',
        read_only=True
    )
    supervisor_role = serializers.CharField(
        source='supervisor.role',
        read_only=True
    )
    log_week_number = serializers.IntegerField(
        source='log.week_number',
        read_only=True
    )
    log_student_name = serializers.CharField(
        source='log.student.username',
        read_only=True
    )

    class Meta:
        model = SupervisorReview
        fields = [
            'id',
            'log',
            'log_week_number',
            'log_student_name',
            'supervisor',
            'supervisor_name',
            'supervisor_role',
            'comments',
            'approved',
        ]
        read_only_fields = ['supervisor']

    def validate_comments(self, value):
        """Ensure comments are not empty."""
        if not value.strip():
            raise serializers.ValidationError(
                "Review comments cannot be empty."
            )
        if len(value) < 10:
            raise serializers.ValidationError(
                "Review comments must be at least 10 characters long."
            )
        return value


class WeeklyLogSerializer(serializers.ModelSerializer):
    """
    Serializer for WeeklyLog model.
    Handles weekly activity logs submitted by student interns.
    Includes full workflow validation for state transitions.
    """
    student_name = serializers.CharField(
        source='student.username',
        read_only=True
    )
    student_email = serializers.CharField(
        source='student.email',
        read_only=True
    )
    placement_company = serializers.CharField(
        source='placement.company_name',
        read_only=True
    )
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    review = SupervisorReviewSerializer(read_only=True)
    can_edit = serializers.SerializerMethodField()
    days_since_submission = serializers.SerializerMethodField()

    class Meta:
        model = WeeklyLog
        fields = [
            'id',
            'placement',
            'placement_company',
            'student',
            'student_name',
            'student_email',
            'week_number',
            'activities',
            'skills_learned',
            'challenges',
            'status',
            'status_display',
            'can_edit',
            'submitted_at',
            'days_since_submission',
            'created_at',
            'updated_at',
            'review',
        ]
        read_only_fields = [
            'student',
            'submitted_at',
            'created_at',
            'updated_at'
        ]

    def get_can_edit(self, obj):
        """
        Checks if the log can still be edited.
        A log can only be edited when it is in Draft status.
        Once submitted, reviewed or approved it is locked.
        """
        return obj.status == 'draft'

    def get_days_since_submission(self, obj):
        """
        Calculates how many days ago the log was submitted.
        Returns None if log has not been submitted yet.
        """
        if obj.submitted_at:
            delta = timezone.now() - obj.submitted_at
            return delta.days
        return None

    def validate_week_number(self, value):
        """Ensure week number is positive."""
        if value <= 0:
            raise serializers.ValidationError(
                "Week number must be a positive number."
            )
        return value

    def validate_activities(self, value):
        """Ensure activities field is not empty."""
        if not value.strip():
            raise serializers.ValidationError(
                "Activities field cannot be empty."
            )
        return value

    def validate(self, data):
        """
        Full validation for weekly log submission.
        Checks:
        1. Activities must be filled before submitting
        2. Skills learned must be filled before submitting
        3. Cannot submit a log that is already approved
        4. Week number must be unique per student per placement
        """
        status = data.get('status', '')
        activities = data.get('activities', '')
        skills_learned = data.get('skills_learned', '')

        # Check 1 and 2: required fields before submitting
        if status == 'submitted':
            if not activities or not activities.strip():
                raise serializers.ValidationError(
                    "Activities field is required before submitting."
                )
            if not skills_learned or not skills_learned.strip():
                raise serializers.ValidationError(
                    "Skills learned field is required before submitting."
                )

        # Check 3: cannot resubmit approved log
        if self.instance and self.instance.status == 'approved':
            raise serializers.ValidationError(
                "This log has been approved and cannot be modified."
            )

        return data


class WeeklyLogSubmitSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for submitting a log.
    Only allows changing status from draft to submitted.
    Used in the submit endpoint.
    """
    class Meta:
        model = WeeklyLog
        fields = ['id', 'status', 'submitted_at']
        read_only_fields = ['submitted_at']

    def validate_status(self, value):
        """Only allow transition from draft to submitted."""
        if self.instance and self.instance.status != 'draft':
            raise serializers.ValidationError(
                "Only logs in Draft status can be submitted."
            )
        if value != 'submitted':
            raise serializers.ValidationError(
                "You can only change status to submitted."
            )
        return value