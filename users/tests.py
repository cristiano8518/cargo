from django.test import TestCase

from users.forms import SignUpForm
from users.models import User
from users.permissions import is_admin_user


class SignUpFormTests(TestCase):
    def test_duplicate_username_is_rejected_case_insensitive(self):
        User.objects.create_user(username="TestUser", password="Pass1234!")
        form = SignUpForm(
            data={
                "username": "testuser",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)


class AdminRoleTests(TestCase):
    def test_regular_user_is_not_admin(self):
        user = User.objects.create_user(username="user1", password="Pass1234!")
        self.assertFalse(is_admin_user(user))

    def test_staff_user_is_admin(self):
        staff = User.objects.create_user(username="staff1", password="Pass1234!", is_staff=True)
        self.assertTrue(is_admin_user(staff))
