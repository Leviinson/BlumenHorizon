from django.test import TestCase


class BaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        pass
