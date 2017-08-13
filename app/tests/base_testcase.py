import os
from django.test import TestCase
from app.tests.creation import Creation


class BaseTestCase(TestCase):

    creation = Creation()

    @classmethod
    def get_test_dir(cls):
        return os.path.dirname(os.path.abspath(__file__))

    def get_arxiv_xml(self, subject='csAI'):
        filename = f'arxiv_{subject}.xml'

        with open(os.path.join(self.get_test_dir(), 'files', filename), 'r') as f:
            xml_text = f.read()

        return xml_text
