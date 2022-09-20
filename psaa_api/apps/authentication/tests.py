from django.test import TestCase

# Create your tests here.
from .models import User

class UserTestClass(TestCase):
    # Setup Method
    def setUp(self):
        self.eric = User(username='Eric', email='eric@gmail.com')

    # Test instance
    def test_instance(self):
        self.assertTrue(isinstance(self.eric, User))

    # Test save method
    def test_save_method(self):
        self.eric.save_user()
        user = User.objects.all()
        self.assertTrue(len(user) > 0)

    # Test delete method
    def tearDown(self):
        User.objects.all().delete()