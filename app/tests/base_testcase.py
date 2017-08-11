from django.test import TestCase
from app.tests.creation import Creation


class BaseTestCase(TestCase):

    creation = Creation()
