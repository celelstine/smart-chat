from django.test import TestCase

from utils.datetime import (
    timezone_exist,
    get_timezone_utc_offset
)


class DateTimeTestCase(TestCase):

    def test_timezone_exist(self):
        self.assertFalse(timezone_exist('unknown time zone'))
        self.assertTrue(timezone_exist('Africa/Bamako'))

    def test_get_timezone_utc_offset(self):
        self.assertEqual(get_timezone_utc_offset('iran'), 4.5)
        self.assertEqual(get_timezone_utc_offset('Asia/Barnaul'), 7.0)
