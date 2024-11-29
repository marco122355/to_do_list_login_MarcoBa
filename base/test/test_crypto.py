# base/test/test_crypto.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch
import requests

class CryptoPricesViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    @patch('requests.get')
    def test_crypto_prices_view_success(self, mock_get):
        # Simula una respuesta exitosa de la API
        mock_response = {
            "bitcoin": {"usd": 50000},
            "ethereum": {"usd": 4000}
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        response = self.client.get(reverse('crypto-prices'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bitcoin: $50000")
        self.assertContains(response, "Ethereum: $4000")

    @patch('requests.get')
    def test_crypto_prices_view_error(self, mock_get):
        # Simula un error en la solicitud a la API
        mock_get.side_effect = requests.exceptions.RequestException("API Error")

        response = self.client.get(reverse('crypto-prices'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No se pudieron obtener los precios de las criptomonedas en este momento.")
