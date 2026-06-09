from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from farmer.models import User


class LoginViewTests(TestCase):
    def test_invalid_login_form_returns_bound_form_instead_of_crashing(self):
        response = self.client.post(reverse("login"), {"username": ""})

        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "Enter a username and password.", status_code=400)
        self.assertTrue(response.context["form"].errors)

    def test_wrong_credentials_return_login_error(self):
        response = self.client.post(
            reverse("login"),
            {"username": "missing", "password": "wrong"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password.")


class RegistrationErrorHandlingTests(TestCase):
    def test_unexpected_user_creation_error_is_not_hidden(self):
        with patch.object(User.objects, "create_user", side_effect=RuntimeError("database down")):
            with self.assertRaisesMessage(RuntimeError, "database down"):
                self.client.post(reverse("register"), {
                    "username": "farmer",
                    "email": "farmer@example.com",
                    "password": "password123",
                    "confirm": "password123",
                    "regcode": "123456",
                })
