from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.urls import reverse
from .serializers import ContactPersonSerializer


class CreateContactTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('create_contact')
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='test_password'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.valid_payload = {
            'name': 'Test Contact',
            'email': 'test_contact@example.com',
            'phone': '1234567890'
        }
        self.invalid_payload = {
            'name': 'Test Contact',
            'email': 'invalid_email',
            'phone': '1234567890'
        }

    def test_create_valid_contact(self):
        response = self.client.post(
            self.url,
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_contact(self):
        response = self.client.post(
            self.url,
            data=self.invalid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
