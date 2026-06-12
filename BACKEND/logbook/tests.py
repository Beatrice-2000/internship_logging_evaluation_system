from django.test import TestCase
from users.models import CustomUser
from placements.models import InternshipPlacement
from logbook.models import WeeklyLog
from datetime import date, timedelta

class WeeklyLogTest(TestCase):
    def setUp(self):
        self.student = CustomUser.objects.create_user(
            username='student', password='pass', role='student'
        )
        self.placement = InternshipPlacement.objects.create(
            student=self.student,
            company_name='Test Co',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=60)
        )

    def test_create_draft_log(self):
        log = WeeklyLog.objects.create(
            student=self.student,
            placement=self.placement,
            week_number=1,
            activities='Test activities',
            status='draft'
        )
        self.assertEqual(log.status, 'draft')
        self.assertIsNone(log.submitted_at)