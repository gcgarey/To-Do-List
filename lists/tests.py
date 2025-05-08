from django.test import TestCase

class TestSmoke(TestCase):
    def test_wrong_math(self):
        self.assertEqual(1 + 1, 3)
