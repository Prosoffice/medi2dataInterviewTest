from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User


class UserRegistrationTestCase(APITestCase):
    def test_user_registration(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
        }
        response = self.client.post("/users/register/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "testuser")


class UserAuthenticationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )

    def test_user_login(self):
        data = {
            "username": "testuser",
            "password": "testpassword",
        }
        response = self.client.post("/users/login/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("token" in response.data)

    def test_user_logout(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/users/logout/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

