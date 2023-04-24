from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .serializers import RegisterSerializer

# Create your tests here.

class RegisterUserAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.valid_payload = {
            'email': 'test@example.com',
            'password': 'test_password',
            'first_name': 'John',
            'last_name': 'Doe',
        }
        self.invalid_payload = {
            'email': 'invalid_email',
            'password': 'test_password',
            'first_name': 'John',
            'last_name': 'Doe',
        }

    def test_create_valid_user(self):
        response = self.client.post(
            self.register_url,
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_user(self):
        response = self.client.post(
            self.register_url,
            data=self.invalid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='test_password'
        )
        self.valid_payload = {
            'email': 'test@example.com',
            'password': 'test_password'
        }
        self.invalid_payload = {
            'email': 'test@example.com',
            'password': 'wrong_password'
        }

    def test_login_valid_user(self):
        response = self.client.post(
            self.login_url,
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_invalid_user(self):
        response = self.client.post(
            self.login_url,
            data=self.invalid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
