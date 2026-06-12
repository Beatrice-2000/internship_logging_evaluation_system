from django.test import TestCase
from users.models import CustomUser
from placements.models import InternshipPlacement
from datetime import date, timedelta

class PlacementModelTest(TestCase):
    def setUp(self):
        self.student = CustomUser.objects.create_user(
            username='student1', password='pass', role='student'
        )

    def test_create_placement(self):
        placement = InternshipPlacement.objects.create(
            student=self.student,
            company_name='Test Co',
            company_address='123 St',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30)
        )
        self.assertEqual(placement.status, 'pending')
        self.assertEqual(placement.student.username, 'student1')