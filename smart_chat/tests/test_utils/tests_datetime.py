from django.test import TestCase

from utils.datetime import timezone_exist


class DateTimeTestCase(TestCase):

    def test_timezone_exist(self, _):
        self.assertFalse(timezone_exist('unknown time zone'))
        self.assertTrue(timezone_exist('Africa/Bamako'))
