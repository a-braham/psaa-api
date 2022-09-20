from django.test import TestCase

# Create your tests here.
from .models import School

class UserTestClass(TestCase):
    # Setup Method
    def setUp(self):
        self.inyange = School(name='inyange')

    # Test instance
    def test_instance(self):
        self.assertTrue(isinstance(self.inyange, School))

    # Test save method
    def test_save_method(self):
        self.inyange.save_school()
        school = School.objects.all()
        self.assertTrue(len(school) > 0)

    # Test delete method
    def tearDown(self):
        School.objects.all().delete()