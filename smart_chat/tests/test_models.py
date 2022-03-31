from django.test import TestCase
from unittest.mock import patch

from smart_chat.models import (
    Store,
    Client
)
from utils.factories import UserFactory


class StoreTestCase(TestCase):

    @patch('smart_chat.models.timezone_exist', return_value=False)
    def test_create_store_invalid_timezone(self, mock_timezone_exist):
        timezone = 'mars/land'
        with self.assertRaises(ValueError):
            Store.objects.create(
                name='store1', phone_number='32222', timezone=timezone)
        mock_timezone_exist.assert_called_with(timezone)

    @patch('smart_chat.models.timezone_exist', return_value=True)
    def test_create_store(self, mock_timezone_exist):
        timezone = 'Africa/Bamako'
        store = Store.objects.create(
            name='store1', phone_number='32222', timezone=timezone)

        self.assertEqual(timezone, store.timezone)


class ClientTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory.create()

    @patch('smart_chat.models.timezone_exist', return_value=False)
    def test_create_client_invalid_timezone(self, mock_timezone_exist):
        timezone = 'mars/land'
        with self.assertRaises(ValueError):
            Client.objects.create(
                user=self.user, phone_number='32222', timezone=timezone)
        mock_timezone_exist.assert_called_with(timezone)

    @patch('smart_chat.models.timezone_exist', return_value=True)
    def test_create_client(self, mock_timezone_exist):
        timezone = 'Africa/Bamako'
        client = Client.objects.create(
            user=self.user, phone_number='32222', timezone=timezone)

        self.assertEqual(timezone, client.timezone)
