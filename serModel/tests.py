from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.urls import reverse
from unittest.mock import patch, MagicMock
from app.models import ContactPerson
from app.serializers import ContactPersonSerializer
import numpy as np


class PredictTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('predict')
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='test_password',
            first_name='Test User',
            phone_number='1234567890'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.contact = ContactPerson.objects.create(
            user=self.user,
            name='Test Contact',
            email='test_contact@example.com',
            phone='0987654321'
        )
        self.payload = {
            'file': 'test_audio_file'
        }

    @patch('app.views.get_feature')
    def test_predict_emotion_fear(self, mock_get_feature):
        mock_get_feature.return_value = np.array([0.5, 0.6, 0.7])
        with patch('app.views.SermodelConfig') as mock_config:
            mock_model = MagicMock()
            mock_model.model.predict.return_value = np.array([[0, 0, 0, 1, 0, 0, 0, 0]])
            mock_config.ser_model = mock_model
            response = self.client.post(
                self.url,
                data=self.payload,
                format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data'], 'fear')
        self.assertEqual(mock_get_feature.call_args[0][0], 'test_audio_file')
        self.assertEqual(mock_model.model.predict.call_args[0][0].shape, (1, 196, 39))

    @patch('app.views.get_feature')
    def test_predict_emotion_not_fear(self, mock_get_feature):
        mock_get_feature.return_value = np.array([0.5, 0.6, 0.7])
        with patch('app.views.SermodelConfig') as mock_config:
            mock_model = MagicMock()
            mock_model.model.predict.return_value = np.array([[0, 0, 0, 0, 0, 1, 0, 0]])
            mock_config.ser_model = mock_model
            response = self.client.post(
                self.url,
                data=self.payload,
                format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data'], 'neutral')
        self.assertEqual(mock_get_feature.call_args[0][0], 'test_audio_file')
        self.assertEqual(mock_model.model.predict.call_args[0][0].shape, (1, 196, 39))

    def test_predict_unauthorized(self):
        self.client.credentials()
        response = self.client.post(
            self.url,
            data=self.payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_predict_missing_payload(self):
        response = self.client.post(
            self.url,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
