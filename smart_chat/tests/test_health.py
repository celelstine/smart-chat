from django.urls import reverse
from django.test import TestCase, Client


class HealthCheckTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_health_check_passes(self):
        resp = self.client.get(reverse('health'))
        self.assertEqual(resp.status_code, 200)
